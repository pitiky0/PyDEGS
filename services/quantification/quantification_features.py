import requests
import dotenv
import os
import time
import json
import pika
import subprocess
import logging
from pathlib import Path
import pandas as pd

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUANTIFICATION_QUEUE = os.getenv("QUANTIFICATION_QUEUE", "quantification_queue")
FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")


def quantification_with_featurescount(bam_file, annotation_file=None):
    """Runs FeatureCounts to quantify the reads in the BAM file using the provided annotation file."""
    # Ensure bam_file is a Path object
    bam_file = Path(bam_file)
    
    # Default annotation file if not provided
    if annotation_file is None:
        annotation_file = "Homo_sapiens.GRCh38.112.gtf"
    else:
        annotation_file = Path(annotation_file)
    
    # Define the output file
    output_file = f"{bam_file}_temp_counts.txt"
    
    logger.info(f"Quantifying {bam_file} with {annotation_file} using FeatureCounts...")

    cmd = [
        "featureCounts",
        "-T", "8",
        "-a", str(annotation_file),
        "-o", str(output_file),
        '-g', 'gene_id',
        str(bam_file)
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)  # Raise an exception if FeatureCounts fails
        # Optionally remove the summary file if not needed
        summary_file = f"{output_file}.summary"
        if os.path.exists(summary_file):
            os.remove(summary_file)
        # Read the count matrix from counts.txt
        count_matrix = pd.read_csv(f"{output_file}", sep='\t', header=0, index_col=0)
        df.to_csv('data.csv')
    except subprocess.CalledProcessError as e:
        logger.error(f"FeatureCounts failed with error code {e.returncode}")
        raise  # Re-raise the exception to stop execution

    logger.info(f"Quantification completed. Output saved to {output_file}")
    return output_file

def download_file(file_name: str):
    """Downloads a file from the given URL and stores it in the current directory."""
    if file_name.endswith(".bam"):
        endpoint = "alignment-files"
    else:
        endpoint = "gtf-gff-files"
    url = f"{FILES_MANAGEMENT_SERVICE}/{endpoint}/download_file/?file_name={file_name}"
    response = requests.get(url, stream=True)
    response.raise_for_status()

    file_path = Path(os.getcwd()) / file_name  # Use Path for better file handling
    with file_path.open('wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logger.info(f"File downloaded to {file_path}")
    return file_path

def upload_file(file_path, user_id):
    """Uploads a file to the specified URL using multipart form-data."""
    url = f"{FILES_MANAGEMENT_SERVICE}/quantification-files/upload_file/?user_id={user_id}"
    with file_path.open('rb') as f:
        files = {'file': (file_path.name, f)}
        response = requests.post(url, files=files)
        response.raise_for_status()

    logger.info(f"File uploaded to {url}")
    return response.json()

def add_tags_to_file(file_name, user_id):
    """Sends a POST request to add tags to the specified file."""
    url = f"{FILES_MANAGEMENT_SERVICE}/alignment-files/add_tags/?file_name={file_name}"
    body = {'tags': {"quantified_by": f"{user_id}"}}
    response = requests.post(url, json=body)
    response.raise_for_status()

    logger.info(f"Tags added to {file_name}")
    return response.json()

def get_file_tags(file_name):
    url = f"{FILES_MANAGEMENT_SERVICE}/quantification-files/get_tags/?file_name={file_name}"
    response = requests.get(url)
    if response.status_code == 404:
        return {}

    response.raise_for_status()
    return response.json()

def add_quantification_tags(file_name, tags):
    """Sends a POST request to add filtering tags to the specified file."""
    url = f"{FILES_MANAGEMENT_SERVICE}/quantification-files/add_tags/?file_name={file_name}"
    body = {'tags': tags}
    response = requests.post(url, json=body)
    response.raise_for_status()

    logger.info(f"Quantification tags added to {file_name}")
    return response.json()

def perform_quantification(bam_file, annotation_file, user_id):
    """Main function to perform quantification of a BAM file."""

    if get_file_tags(f"{bam_file}_counts.csv").get("tags"):
        logger.info(f"Skipping {bam_file}: File already quantified")
        return

    bam_file_path = download_file(bam_file)
    annotation_file_path = download_file(annotation_file) if annotation_file is not None else None

    try:
        quantification_result = quantification_with_featurescount(bam_file_path, annotation_file_path)
        input_q = quantification_result.split("/")[-1]
        subprocess.run(f"cat {input_q} | cut -f1,7 | tail -n +2 > {bam_file}_counts.csv", shell=True, check=True)
        quantification_result = f"{bam_file}_counts.csv"
        quantification_result_path = Path(os.getcwd()) / quantification_result  # Use Path for better file handling
        tags = {"origin_file": str(bam_file)}
        upload_response = upload_file(quantification_result_path, user_id)
        quantification_result = quantification_result.split("/")[-1]  # Get the filename only
        add_quantification_tags(quantification_result, tags)
        add_tags_to_file(bam_file, user_id)
        logger.info(f"Upload successful. Response: {upload_response}")
        os.remove(quantification_result_path)  # Remove the temporary file after upload
    except (subprocess.CalledProcessError, requests.exceptions.RequestException) as e:
        logger.error(f"Processing failed for {bam_file}: {e}")
    finally:
        if os.path.exists(bam_file_path):
            os.remove(bam_file_path)
        if annotation_file_path is not None:
            if os.path.exists(annotation_file_path):
                os.remove(annotation_file_path)

# Function to process messages from the RabbitMQ queue
def process_message(message):
    try:
        bam_file = message["bam_file"]
        annotation_file = message.get("annotation_file")  # Use .get() for optional annotation file
        user_id = message["user_id"]

        # Perform quantification if file types are supported
        if bam_file.endswith(".bam"):
            if annotation_file is not None:
                if any(ann_file in annotation_file for ann_file in [".gtf", ".gff"]):
                    perform_quantification(bam_file, annotation_file, user_id)
            else:
                perform_quantification(bam_file, annotation_file, user_id)  # Pass None if no annotation file
            logger.info(f" [x] Processed {message}")
        else:
            logger.info(f" [x] Skipping {bam_file} and {annotation_file}: Unsupported file type")

    except Exception as e:
        logger.error(f"Error processing message {message}: {e}")

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        process_message(message)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
    except Exception as e:
        logger.error(f"Error in callback: {e}")

# Function to set up and consume messages from the RabbitMQ queue
def consume_from_queue():
    max_retries = 5
    retry_interval = 10  # Seconds

    for attempt in range(max_retries):
        try:
            connection_params = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                heartbeat=600,  # Set a suitable heartbeat interval (in seconds)
                blocked_connection_timeout=300  # Set a timeout for blocked connections (in seconds)
            )
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()

            # Declare the queue (no need to declare an exchange for the default one)
            channel.queue_declare(queue=QUANTIFICATION_QUEUE, durable=True)

            # Start consuming from the queue using the default exchange
            channel.basic_consume(
                queue=QUANTIFICATION_QUEUE, on_message_callback=callback, auto_ack=True
            )

            logger.info(" [*] Waiting for quantification messages. To exit press CTRL+C")
            channel.start_consuming()  # Start consuming messages (blocks until stopped)

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Attempt {attempt + 1}/{max_retries}: RabbitMQ not ready yet. Error: {e}")
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
        else:
            break  # If no exception occurred, connection was successful, exit the loop
    else:
        # This block runs if the for loop completes without a 'break' (all retries failed)
        raise Exception("Could not connect to RabbitMQ after multiple attempts.")

if __name__ == '__main__':
    try:
        consume_from_queue()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)