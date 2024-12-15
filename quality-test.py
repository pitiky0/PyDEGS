import pika
import json

RABBITMQ_HOST = "localhost"
QUALITY_CONTROL_QUEUE = "quality_control_queue"

def send_message(file_name, user_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    message = {
        "filename": file_name,
        "user_id": user_id
    }

    channel.basic_publish(
        exchange='',
        routing_key=QUALITY_CONTROL_QUEUE,
        body=json.dumps(message)
    )

    print(" [x] Sent message: %s", message)
    connection.close()


# Example usage
filename = "13681.fastq.gz"
user_id = 1000
send_message(filename, user_id)

print( {"message": "Quality control request sent"})
