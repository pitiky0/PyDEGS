import requests
import os
import dotenv
import gzip
import logging
import tempfile
import subprocess
from Bio import SeqIO
from math import log2
from collections import Counter

dotenv.load_dotenv()

# Set up and Configure logging
logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
FILTERING_FASTQ_EXCHANGE = os.getenv("FILTERING_FASTQ_EXCHANGE", "filtering_fastq_exchange")
FILTERING_FASTQ_QUEUE = os.getenv("FILTERING_FASTQ_QUEUE", "filtering_fastq_queue")
FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")

def get_file_path(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    return file_path

def custom_hash(params):
    """Generates a simple custom hash based on the input parameters."""
    hash_value = 0
    for param in params:
        param_str = str(param) if param is not None else ""
        for char in param_str:
            hash_value += ord(char)
            hash_value = hash_value * 31 % (2 ** 32)  # Keep hash value in the range of 32-bit integer
    return hash_value

def filter_fastq(input_files, output_files, is_paired_end, truncate_start_bases=0, truncate_end_bases=0,
                 left_adapter=None, right_adapter=None, min_length=0, complexity=0,
                 sliding_window_size=4, sliding_window_quality=15):

    # Create a temporary adapter file if adapters are provided
    if left_adapter or right_adapter:
        with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
            if left_adapter:
                f.write(f">left_adapter\n{left_adapter}\n")
            if right_adapter:
                f.write(f">right_adapter\n{right_adapter}\n")
        adapters_file = f.name
    else:
        adapters_file = None

    output_files = [str(get_file_path(file)) for file in output_files]

    # Build the Trimmomatic command
    command = [
        "java", "-jar", "Trimmomatic-0.39/trimmomatic-0.39.jar"
    ]

    if is_paired_end:
        command.extend(["PE", "-threads", "8", input_files[0], input_files[1], 
                        output_files[0], output_files[1], output_files[2], output_files[3]])
    else:
        command.extend(["SE", "-threads", "8", input_files[0], output_files[0]])
    unique_id = output_files[0].split("_")[1]
    command.extend([
        "-trimlog", f"{get_file_path(f'{unique_id}_trimlog.txt')}",
        "-summary", f"{get_file_path(f'{unique_id}_summary.txt')}",
    ])
    # Add adapter trimming if necessary
    if adapters_file:
        command.extend([
            f"ILLUMINACLIP:{adapters_file}:2:30:10"
        ])
    elif is_paired_end:
        command.extend([
            f"ILLUMINACLIP:TruSeq3-PE.fa:2:30:10"
        ])
    else:
        command.extend([
            f"ILLUMINACLIP:TruSeq3-SE.fa:2:30:10"
        ])

    # Add truncation options
    if truncate_start_bases > 0:
        command.extend([f"LEADING:{truncate_start_bases}"])
    if truncate_end_bases > 0:
        command.extend([f"TRAILING:{truncate_end_bases}"])

    command.extend([f"MAXINFO:40:{complexity}"])

    # Add sliding window trimming
    if sliding_window_size and sliding_window_quality:
        command.extend([
            f"SLIDINGWINDOW:{sliding_window_size}:{sliding_window_quality}"
        ])

    # Add minimum length filter
    if min_length > 0:
        command.extend([f"MINLEN:{min_length}"])

    # Run the Trimmomatic command
    result = subprocess.run(command)
    if result.returncode != 0:
        logger.error(f"Trimmomatic failed with exit code {result.returncode}")
        return

    # Remove the temporary adapter file if it was created
    if adapters_file:
        os.remove(adapters_file)

def download_file(file_name: str):
    """
    Downloads a file from the given URL and stores it in the current directory.

    Args:
        file_name (str): The name to save the downloaded file as.

    Returns:
        str: The path to the downloaded file.
    """
    if file_name.startswith("filtered"):
        url = f"{FILES_MANAGEMENT_SERVICE}/filtered-fastq-files/download_file/?file_name={file_name}"
    else:
        url = f"{FILES_MANAGEMENT_SERVICE}/fastq-files/download_file/?file_name={file_name}"
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure we notice bad responses
    file_name = file_name.split("/")[-1]
    file_path = str(get_file_path(file_name))

    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logger.info(f"File downloaded to {file_path}")
    return file_path

def upload_file(file_path, user_id):
    """
    Uploads a file to the specified URL using multipart form-data.

    Args:
        file_path (str): Path to the file to upload.
        user_id (int): User ID for the upload.

    Returns:
        dict: Response dictionary containing upload details (may vary depending on API).
    """
    url = f"{FILES_MANAGEMENT_SERVICE}/filtered-fastq-files/upload_file/?user_id={user_id}"
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise exception for non-200 status codes

    return response.json()  # Assuming response is JSON

def add_tags_to_file(file_name, user_id):
    """
    Sends a POST request to add tags to the specified file.

    Args:
        file_name (str): The name of the file to add tags to.
        user_id (int): The user ID to associate with the tags.

    Returns:
        dict: The response from the server.
    """
    if file_name.startswith("filtered"):
        url = f"{FILES_MANAGEMENT_SERVICE}/filtered-fastq-files/add_tags/?file_name={file_name}"
    else:
        url = f"{FILES_MANAGEMENT_SERVICE}/fastq-files/add_tags/?file_name={file_name}"

    body = {'tags': {"filtered_by": f"{user_id}"}}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Tags added to {file_name}")
    return response.json()

def get_file_tags(file_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/filtered-fastq-files/get_tags/?file_name={file_name}"

    response = requests.get(url)
    # response.raise_for_status()  # Raise an error for bad status codes

    if response.status_code == 404:
        return {}

    return response.json()

def add_filtering_tags(file_name, tags):
    """
    Sends a POST request to add filtering tags to the specified file.

    Args:
        file_name (str): The name of the file to add tags to.
        tags (dict): The tags to add to the file.

    Returns:
        dict: The response from the server.
    """
    url = f"{FILES_MANAGEMENT_SERVICE}/filtered-fastq-files/add_tags/?file_name={file_name}"
    body = {'tags': tags}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Filtering tags added to {file_name}")
    return response.json()

def perform_filtering_fastq(files, user_id, is_paired_end, truncate_start_bases, truncate_end_bases,
                     left_adapter, right_adapter, min_length, n_bases, complexity):
    files_to_download = files
    temp_files = []
    for file in files:
        if "/" in file:
            temp_files.append(file.split("/")[-1])
        else:
            temp_files.append(file)
    logger.info(f"Temp files: {temp_files}")
    logger.info(f"Files to download: {files_to_download}")
    files = temp_files

    # Generate a custom hash
    unique_id = custom_hash([truncate_start_bases, truncate_end_bases, left_adapter,
                             right_adapter, min_length, n_bases, complexity])

    if is_paired_end:
        filtred_file_name_forward_paired = f"filtered_{unique_id}_{files[0].split('.fastq.gz')[0]}_forward_paired.fastq.gz"
        filtred_file_name_reverse_paired = f"filtered_{unique_id}_{files[0].split('.fastq.gz')[0]}_reverse_paired.fastq.gz"
        body1 = get_file_tags(filtred_file_name_forward_paired)
        body2 = get_file_tags(filtred_file_name_reverse_paired)
        if "tags" in body1 and "tags" in body2:
            # File already filtered with the same parameters, we don't need to re-filter the file
            logger.info(f"Skipping {files}: Files already filtered with the same parameters")
            return
    else:
        body = get_file_tags(f"filtered_{unique_id}_{files[0]}")
        if "tags" in body:
            # File already filtered with the same parameters, we don't need to re-filter the file
            logger.info(f"Skipping {files[0]}: File already filtered with the same parameters")
            return

    input_files = [download_file(file) for file in files_to_download]

    if is_paired_end:
        filtred_file_name_forward_unpaired = f"filtered_{unique_id}_{files[0].split('.fastq.gz')[0]}_forward_unpaired.fastq.gz"
        filtred_file_name_reverse_unpaired = f"filtered_{unique_id}_{files[0].split('.fastq.gz')[0]}_reverse_unpaired.fastq.gz"

        output_files = [filtred_file_name_forward_paired, filtred_file_name_forward_unpaired, filtred_file_name_reverse_paired, filtred_file_name_reverse_unpaired]
        # Run the filter_fastq command for both forward and reverse reads
        filter_fastq(files, output_files, is_paired_end, truncate_start_bases, truncate_end_bases,
                     left_adapter, right_adapter, min_length, complexity)
        
        tags = {
            "origin_file": str(" ".join(files)),
            "truncate_bases": f"start:{str(truncate_start_bases)} end:{str(truncate_end_bases)}",
            "adapters": f"left:{str(left_adapter)} right:{str(right_adapter)}",
            "min_length": str(min_length),
            "complexity": str(complexity)
        }

        try:
            upload_response1 = upload_file(output_files[0], user_id)
            upload_response2 = upload_file(output_files[2], user_id)
            upload_response3 = upload_file(f"{unique_id}_trimlog.txt", user_id)
            upload_response4 = upload_file(f"{unique_id}_summary.txt", user_id)
            logger.info(f"Upload successful. Response: {upload_response1} {upload_response2}")
            add_filtering_tags(filtred_file_name_forward_paired, tags)
            add_filtering_tags(filtred_file_name_reverse_paired, tags)
            logger.info(f"tags added to {filtred_file_name_forward_paired} and {filtred_file_name_reverse_paired}")
        except requests.exceptions.RequestException as e:
            logger.info(f"Upload failed:{tags} {e}")

    else:
        filtred_file_name = f"filtered_{unique_id}_{files[0]}"
        output_files = [filtred_file_name]
        filter_fastq(input_files, output_files, False, truncate_start_bases, truncate_end_bases,
                        left_adapter, right_adapter, min_length, complexity)
        
        tags = {
            "origin_file": str(files[0]),
            "truncate_bases": f"start:{str(truncate_start_bases)} end:{str(truncate_end_bases)}",
            "adapters": f"left:{str(left_adapter)} right:{str(right_adapter)}",
            "min_length": str(min_length),
            "complexity": str(complexity)
        }

        try:
            upload_response = upload_file(filtred_file_name, user_id)
            upload_response3 = upload_file(f"{unique_id}_trimlog.txt", user_id)
            upload_response4 = upload_file(f"{unique_id}_summary.txt", user_id)
            logger.info(f"Upload successful. Response: {upload_response}")
            add_filtering_tags(filtred_file_name, tags)
            logger.info(f"tags added to {filtred_file_name}")
        except requests.exceptions.RequestException as e:
            logger.info(f"Upload failed:{tags} {e}")
    
    # Add tags to the original file
    for file_name in files_to_download:
        add_tags_to_file(file_name, user_id)
        
    for file in input_files:
        os.remove(file)

    for file in output_files:
        os.remove(file)

    os.remove(get_file_path(f"{unique_id}_trimlog.txt"))
    os.remove(get_file_path(f"{unique_id}_summary.txt"))

    