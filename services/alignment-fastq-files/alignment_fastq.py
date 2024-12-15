import requests
import dotenv
import os
import subprocess
import logging
from pathlib import Path
from typing import Union, List

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
ALIGNMENT_FASTQ_QUEUE = os.getenv("ALIGNMENT_FASTQ_QUEUE", "alignment_fastq_queue")
FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")

def get_file_path(file_name):
    return Path(os.getcwd()) / file_name

def align_fastq_to_genome(fastq_files: Union[str, List[str]], reference_file: str, is_paired: bool = False):
    """Aligns a single FASTQ file to a reference genome using HISAT2."""

    # create index for reference genome
    subprocess.run(["./indexing_hisat2.sh", f"{reference_file}"], check=True)

    if is_paired:
        if len(fastq_files) % 2 != 0:
            raise ValueError("Paired-end FASTQ files must be provided in pairs.")
        fastq_files.sort()

    output_bam = Path(fastq_files[0]).with_suffix('.bam')
    output_dir = Path(fastq_files[0]).with_suffix('')
    if reference_file is None:
     reference_genome_file = "grch38_genome/grch38"
    logger.info(f"Aligning {fastq_files} to {reference_file} ...")
    ref = reference_file.split(".")[:-2]
    ref = ".".join(ref)
    logger.info(f"Reference genome: {ref}")
    subprocess.run(["./run_hisat2.sh", f"index/{ref}*", f"{output_dir}", f"{fastq_files[0]}"], check=True)
    logger.info(f"Alignment complete. Output: {output_dir}/")
    return output_dir

def download_file(file_name: str):
    """Downloads a file from the given URL and stores it in the current directory."""
    if file_name and any(file_name.endswith(ex) for ex in [".fastq.gz", ".fastq", ".fq.gz", ".fq"]):
        endpoint = "filtered-fastq-files" if file_name.startswith("filtered") else "fastq-files"
    else:
        endpoint = "reference-genomes-files"
    url = f"{FILES_MANAGEMENT_SERVICE}/{endpoint}/download_file/?file_name={file_name}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    file_path = get_file_path(file_name)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logger.info(f"File downloaded to {file_path}")
    return file_path

def upload_file(file_path, user_id):
    """Uploads a file to the specified URL using multipart form-data."""
    url = f"{FILES_MANAGEMENT_SERVICE}/alignment-files/upload_file/?user_id={user_id}"
    with open(file_path, 'rb') as f:
        files = {'file': (file_path, f)}
        response = requests.post(url, files=files)
        response.raise_for_status()

    logger.info(f"File uploaded to {url}")
    return response.json()

def add_tags_to_file(file_name, user_id):
    """Sends a POST request to add tags to the specified file."""
    endpoint = "filtered-fastq-files" if file_name.startswith("filtered") else "fastq-files"
    url = f"{FILES_MANAGEMENT_SERVICE}/{endpoint}/add_tags/?file_name={file_name}"
    body = {'tags': {"aligned_by": f"{user_id}"}}
    response = requests.post(url, json=body)
    response.raise_for_status()

    logger.info(f"Tags added to {file_name}")
    return response.json()

def get_file_tags(file_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/alignment-files/get_tags/?file_name={file_name}"
    response = requests.get(url)
    if response.status_code == 404:
        return {}

    response.raise_for_status()
    return response.json()

def add_alignment_tags(file_name, tags):
    """Sends a POST request to add filtering tags to the specified file."""
    url = f"{FILES_MANAGEMENT_SERVICE}/alignment-files/add_tags/?file_name={file_name}"
    body = {'tags': tags}
    response = requests.post(url, json=body)
    response.raise_for_status()

    logger.info(f"Filtering tags added to {file_name}")
    return response.json()

def perform_alignment_fastq(fastq_files, reference_file, is_paired, user_id):
    """Main function to perform alignment of a FASTQ file to a reference genome."""

    files = []
    for file in fastq_files:
        if isinstance(file, str):
            file = file.split("/")[-1] if "/" in file else file
            if file.startswith("filtered"):
                file = file.split("_")[2:]
                file = "_".join(file)
            files.append(file)
        elif isinstance(file, tuple):
            file1 = file[0][0].split("/")[-1] if "/" in file[0][0] else file[0][0]
            file2 = file[0][1].split("/")[-1] if "/" in file[0][1] else file[0][1]
            my_tuple = (file1, file2)
            if file[0][0].startswith("filtered"):
                tuple_file = file[0][0].split("_")[2:]
                tuple_file = "_".join(file)
                my_tuple = (tuple_file, my_tuple[1])
            if file[0][1].startswith("filtered"):
                tuple_file = file[0][1].split("_")[2:]
                tuple_file = "_".join(file)
                my_tuple = (my_tuple[0], tuple_file)
            files.append(my_tuple)
    fastq_files = files
    logger.info(f"Performing alignment for {fastq_files} ...")
    if not is_paired:
        bam_files = [file.replace(".fastq.gz", ".bam") for file in files]
    else:
        bam_files = [file.replace(".fastq.gz", ".bam") for file in files]

    for bam_file in bam_files:
        if get_file_tags(bam_file).get("tags"):
            logger.info(f"Skipping {fastq_files}: File already aligned")
            return
    temp_files = []
    for fastq_file in fastq_files:  
        fastq_file_path = download_file(fastq_file)
        temp_files.append(fastq_file_path)
    fastq_files = temp_files

    if reference_file is not None:
        reference_file_path = download_file(reference_file)
    try:
        output_dir = align_fastq_to_genome(fastq_files, reference_file, is_paired)
        tags = {"origin_file": str(fastq_file[0])}
        for file in os.listdir(f"{output_dir}"):
            upload_response = upload_file(f"{output_dir}/{file}", user_id)
            add_alignment_tags(f"{output_dir}/{file}", tags)
            logger.info(f"Upload successful. Response: {upload_response}")
    except (subprocess.CalledProcessError, requests.exceptions.RequestException) as e:
        logger.error(f"Processing failed for {fastq_file}: {e}")
    
    add_tags_to_file(fastq_file, user_id)
    # fastq_file_path.unlink()
    if reference_file_path:
        # remove extension from reference file
        reference_file_path = reference_file_path.with_suffix('')
        # reference_file_path.unlink()
    # bam_file.unlink(missing_ok=True)
    # run rm -r on output_dir
    # subprocess.run(["rm", "-r", f"{output_dir}"], check=True)
    subprocess.run(["rm", "-r", "index/"], check=True)
    

