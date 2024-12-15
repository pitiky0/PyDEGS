import requests
import os
import subprocess
import dotenv
import logging
from typing import Union, List
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUALITY_CONTROL_EXCHANGE = os.getenv("QUALITY_CONTROL_EXCHANGE", "quality_control_exchange")
QUALITY_CONTROL_QUEUE = os.getenv("QUALITY_CONTROL_QUEUE", "quality_control_queue")
FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")


def run_fastqc(output_dir: str, threads: int = None):
    """
    Runs FastQC on the given input file(s) and saves the output to the specified directory.

    Args:
        output_dir (str): Path to the output directory for FastQC results.
        threads (int, optional): Number of threads to use for parallel processing. Defaults to None (single thread).
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Use glob to expand the input pattern
    input_files = glob.glob("*.fastq.gz")
    if not input_files:
        logger.error(f"No files matching the pattern '.fastq.gz' were found.")
        return
    
    # Construct FastQC command with optional threading argument
    command = ["fastqc"]
    if threads:
        command += ["-t", str(threads)]
    command += ["-o", output_dir] + input_files
    logger.info(f"Running FastQC with command: {' '.join(command)}")
    # Execute FastQC command with capture output
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logger.info(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running FastQC: {e.stderr}")
        raise

    logger.info(f"FastQC completed and the result saved to {output_dir}")

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

    file = file_name.split("/")[-1]
    current_dir = os.getcwd()
    file = os.path.join(current_dir, file)
    with open(file, 'wb') as opened_file:
        for chunk in response.iter_content(chunk_size=8192):
            opened_file.write(chunk)
        opened_file.close()

    logger.info(f"File downloaded to {file}")
    return file

def upload_file(file_path, user_id, folder_name):
    """
    Uploads a file to the specified URL using multipart form-data.

    Args:
        file_path (str): Path to the file to upload.
        user_id (int): User ID for the upload.
        folder_name (str): Name of the folder to upload the file to.

    Returns:
        dict: Response dictionary containing upload details (may vary depending on API).
    """
    url = f"{FILES_MANAGEMENT_SERVICE}/quality-control-files/upload_file/?user_id={user_id}&folder_name={folder_name}"
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise exception for non-200 status codes

    logger.info(f"File uploaded to {url}")
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

    body = {'tags': {"controled_by": f"{user_id}"}}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Tags added to {file_name}")
    return response.json()

def get_file_tags(file_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/quality-control-files/get_tags/?file_name={file_name}"

    response = requests.get(url)
    # response.raise_for_status()  # Raise an error for bad status codes

    if response.status_code == 404:
        return {}

    return response.json()

def add_quality_control_tags(file_name, tag):
    """
    Sends a POST request to add quality control tags to the specified file.

    Args:
        file_name (str): The name of the file to add tags to.

    Returns:
        dict: The response from the server.
    """
    url = f"{FILES_MANAGEMENT_SERVICE}/quality-control-files/add_tags/?file_name={file_name}"
    body = {'tags': {'origin_file': tag}}

    response = requests.post(url, json=body)
    response.raise_for_status()  # Raise an error for bad status codes

    logger.info(f"Quality control tags added to {file_name}")
    return response.json()

def perform_quality_control(files: Union[str, List[str]], user_id: str):
    logger.info(f"Performing quality control on files: {files}")
    # Ensure files is a list
    if isinstance(files, str):
        files = [files]

    folders = [file.split("/")[-1].replace(".fastq.gz", "_fastqc") for file in files]
    controled_files = [f"{folder}/{folder}.zip" for folder in folders]

    # check if the file is already controled or not
    for controled_file in controled_files:
        body = get_file_tags(controled_file)
        if "tags" in body.keys():
            if body['tags']['origin_file'] in files:
                logger.info(f"File {body['tags']['origin_file']} already controled")
                files.remove(body['tags']['origin_file'])

    file_paths = [download_file(file) for file in files]
    logger.info(f"File paths: {file_paths}")
    output_dir = "fastqc_output/"
    run_fastqc(output_dir, 8)  # Add threads argument if needed
    logger.info(os.listdir(output_dir))
    # Loop through all files in the output_dir
    for i, file in enumerate(os.listdir(output_dir)):
        if file.endswith("html") or file.endswith("zip"):
            logger.info(f"Uploading file: {file}")
            output_file_path = os.path.join(output_dir, file)
            try:
                upload_response = upload_file(output_file_path, user_id, f"{file.split('_fastqc')[0]}_fastqc")
                logger.info(f"Upload successful. Response: {upload_response}")
                add_quality_control_tags(f"{file.split('_fastqc')[0]}_fastqc/{file}", f"{file.split('_fastqc')[0]}.fastq.gz")
            except requests.exceptions.RequestException as e:
                logger.info(f"Upload failed: {e}")

    [add_tags_to_file(file, user_id) for file in files]

    # Remove the downloaded file
    [os.remove(file.split("/")[-1]) for file in files]

    # Remove the output directory and all its contents
    os.system(f"rm -r {output_dir}")
    