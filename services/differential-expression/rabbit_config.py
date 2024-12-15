import json
import os
import sys
import pika
import time
from diffExp import perform_diff_expression, RABBITMQ_HOST, DIFF_EXPRESSION_QUEUE
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_message(message):
    try:
        file_name = message["file_name"]
        user_id = message["user_id"]
        metadata = message["metadata"]
        conditions = message["condition"]

        # Perform filtering fastq files
        if any(ex in file_name for ex in [".txt", ".csv"]):
            perform_diff_expression(file_name, int(user_id), metadata, [conditions])
            logger.info(f" [x] Processed {message}")
        else:
            logger.info(f" [x] Skipping {file_name}: Unsupported file type")
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
            channel.queue_declare(queue=DIFF_EXPRESSION_QUEUE, durable=True)

            # Start consuming from the queue using the default exchange
            channel.basic_consume(
                queue=DIFF_EXPRESSION_QUEUE, on_message_callback=callback, auto_ack=True
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
