import os
import dotenv
import pika
import json

dotenv.load_dotenv()


FILES_MANAGEMENT_SERVICE = os.getenv("FILES_MANAGEMENT_SERVICE", "http://localhost:8003/files")
AUTH_SERVICE = os.getenv("AUTH_SERVICE", "http://localhost:8002/auth")
USER_MANAGEMENT_SERVICE = os.getenv("USER_MANAGEMENT_SERVICE", "http://localhost:8001/user")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
FILTERING_FASTQ_QUEUE = "filtering_fastq_queue"
QUALITY_CONTROL_QUEUE = "quality_control_queue"
ALIGNMENT_FASTQ_QUEUE = "alignment_fastq_queue"
QUANTIFICATION_QUEUE = "quantification_queue"
DIFF_EXPRESSION_QUEUE = "diff_expression_queue"

def send_message(message, queue):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
            )
        )

        print(" [x] Sent message: %s", message)
        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection.is_open:
            connection.close()
