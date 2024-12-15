from flask import Flask, request, jsonify
import os
import dotenv
import pika
import json
import contextlib
from flask_cors import CORS

dotenv.load_dotenv()

app = Flask(__name__)
CORS(app)

RABBITMQ_HOST = "localhost"
QUALITY_CONTROL_EXCHANGE = "quality_control_exchange"
QUALITY_CONTROL_QUEUE = "quality_control_queue"

@contextlib.contextmanager
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=QUALITY_CONTROL_EXCHANGE, exchange_type='direct')
    channel.queue_declare(queue=QUALITY_CONTROL_QUEUE)
    channel.queue_bind(exchange=QUALITY_CONTROL_EXCHANGE, queue=QUALITY_CONTROL_QUEUE)

    try:
        yield channel
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        connection.close()

def perform_quality_control(filename, user_id):
    message = json.dumps({"filename": filename, "user_id": user_id})
    with get_rabbitmq_channel() as channel:
        channel.basic_publish(
            exchange=QUALITY_CONTROL_EXCHANGE, routing_key=QUALITY_CONTROL_QUEUE, body=message
        )
        print(f" [x] Sent quality control request for {filename}")
    return {"message": "Quality control request sent"}

@app.route('/quality-control', methods=['POST'])
def quality_control():
    data = request.json
    filename = data.get('filename')
    user_id = data.get('user_id')
    result = perform_quality_control(filename, user_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
