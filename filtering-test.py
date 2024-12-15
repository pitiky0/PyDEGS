import pika
import json

RABBITMQ_HOST = "localhost"
FILTERING_FASTQ_QUEUE = "filtering_fastq_queue"

def send_message(file_name, user_id, truncate_start_bases, truncate_end_bases, 
                 left_adapter, right_adapter, min_length, n_bases, complexity):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()

        message = {
            "file_name": file_name,
            "user_id": user_id,
            "truncate_start_bases": truncate_start_bases,
            "truncate_end_bases": truncate_end_bases,
            "left_adapter": left_adapter,
            "right_adapter": right_adapter,
            "min_length": min_length,
            "n_bases": n_bases,
            "complexity": complexity
        }

        channel.basic_publish(
            exchange='',
            routing_key=FILTERING_FASTQ_QUEUE,
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

if __name__ == "__main__":
    file_name = "13681.fastq.gz"
    user_id = 1000
    truncate_start_bases = 5
    truncate_end_bases = 5
    left_adapter = "ACCCGCTGGCC"
    right_adapter = "ACCCGCTGGCC"
    min_length = 40
    n_bases = 0
    complexity = 0.5

    send_message(file_name, user_id, truncate_start_bases, truncate_end_bases,
                 left_adapter, right_adapter, min_length, n_bases, complexity)
    print("Filtering request sent")
