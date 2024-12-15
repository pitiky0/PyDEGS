import json
import os
import sys
import pika
import time
from filtering_fastq import perform_filtering_fastq, RABBITMQ_HOST, FILTERING_FASTQ_QUEUE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_message(message):
    try:
        files = message["files"]
        user_id = message["user_id"]
        is_paired_end = message["is_paired_end"]
        truncate_start_bases = message["truncate_start_bases"]
        truncate_end_bases = message["truncate_end_bases"]
        left_adapter = message["left_adapter"]
        right_adapter = message["right_adapter"]
        min_length = message["min_length"]
        n_bases = message["n_bases"]
        complexity = message["complexity"]

        # Validate input
        if not files or not user_id:
            raise ValueError("Missing required fields in message")

        if left_adapter or right_adapter or min_length or n_bases or complexity or truncate_start_bases or truncate_end_bases:
            # If any of these fields are provided, that means the user wants to perform filtering
            pass
        else:
            logger.info(f" [x] Skipping {message}")
            return

        if is_paired_end:
            if len(files) != 2:
                raise ValueError("Paired-end files must have exactly 2 files")

        if int(truncate_start_bases):
            if truncate_start_bases < 0:
                raise ValueError("Truncate bases must be non-negative")
            
        if int(truncate_end_bases):
            if truncate_end_bases < 0:
                raise ValueError("Truncate bases must be non-negative")
    
        if int(min_length) < 0:
            raise ValueError("Minimum length must be non-negative")
        
        if int(n_bases) < 0:
            raise ValueError("N bases must be non-negative")

        if left_adapter:
            if not left_adapter.isalpha():
                raise ValueError("Left adapter must be a string")
            
        if right_adapter:
            if not right_adapter.isalpha():
                raise ValueError("Right adapter must be a string")
        
        if complexity:
            if float(complexity) < 0 or float(complexity) > 1:
                raise ValueError("Complexity must be a float between 0 and 1")
            
        if isinstance(files, str):
            files = [files]

        # Perform filtering fastq files
        perform_filtering_fastq(files, user_id, is_paired_end, int(truncate_start_bases), int(truncate_end_bases),
                                left_adapter, right_adapter, int(min_length), int(n_bases), float(complexity))
        logger.info(f" [x] Processed {message}")
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

def main():
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
            channel.queue_declare(queue=FILTERING_FASTQ_QUEUE, durable=True)

            # Start consuming from the queue using the default exchange
            channel.basic_consume(
                queue=FILTERING_FASTQ_QUEUE, on_message_callback=callback, auto_ack=True
            )

            logger.info(" [*] Waiting for messages. To exit press CTRL+C")
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
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
