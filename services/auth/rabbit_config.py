import os
import dotenv
import pika
import json  # For serializing messages
import contextlib

dotenv.load_dotenv()

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
EMAIL_EXCHANGE = "email_exchange"
EMAIL_QUEUE = "email_queue"


# Context manager for easier connection handling
@contextlib.contextmanager
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EMAIL_EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=EMAIL_QUEUE)
    channel.queue_bind(exchange=EMAIL_EXCHANGE, queue=EMAIL_QUEUE)  # Bind queue to exchange

    try:
        yield channel  # Code using the channel will run here
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()


async def send_email_verification(email, token):
    message = json.dumps({"type": "email_verification", "email": email, "token": token})
    with get_rabbitmq_channel() as channel:
        channel.basic_publish(
            exchange=EMAIL_EXCHANGE, routing_key=EMAIL_QUEUE, body=message
        )
        print(f" [x] Sent email verification for {email}")
    return {"message": "Verification email sent"}

async def send_password_reset_email(email, token):
    message = json.dumps({"type": "password_reset", "email": email, "token": token})

    with get_rabbitmq_channel() as channel:
        channel.basic_publish(
            exchange=EMAIL_EXCHANGE, routing_key=EMAIL_QUEUE, body=message
        )
        print(f" [x] Sent password reset email for {email}")
    return {"message": "Password reset email sent"}

