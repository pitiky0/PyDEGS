import json
import os
import sys
import dotenv
import pika
import time
from email_handler import send_verification_email, send_password_reset_email
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
EMAIL_EXCHANGE = os.getenv("EMAIL_EXCHANGE", "email_exchange")
EMAIL_QUEUE = os.getenv("EMAIL_QUEUE", "email_queue")

def process_message(message):
    email = message["email"]
    token = message["token"]

    if message["type"] == "email_verification":
        send_verification_email(email, token)
    elif message["type"] == "password_reset":
        send_password_reset_email(email, token)

    logger.info(f" [x] Processed {message}")

def callback(ch, method, properties, body):
    message = json.loads(body)
    process_message(message)

def main():
    max_retries = 5
    retry_interval = 10  # Seconds

    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            channel = connection.channel()

            channel.exchange_declare(exchange=EMAIL_EXCHANGE, exchange_type="direct")
            channel.queue_declare(queue=EMAIL_QUEUE)
            channel.queue_bind(exchange=EMAIL_EXCHANGE, queue=EMAIL_QUEUE)

            channel.basic_consume(
                queue=EMAIL_QUEUE, on_message_callback=callback, auto_ack=True
            )

            logger.info(" [*] Waiting for messages. To exit press CTRL+C")
            channel.start_consuming()  # Start consuming messages (blocks until stopped)

        except pika.exceptions.AMQPConnectionError as e:
            logger.info(f"Attempt {attempt + 1}/{max_retries}: RabbitMQ not ready yet. Error: {e}")
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
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