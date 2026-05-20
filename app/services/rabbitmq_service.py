import os
import json
import pika

from dotenv import load_dotenv


load_dotenv()


RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL"
)

QUEUE_NAME = "analysis_jobs"


def get_connection():
    if not RABBITMQ_URL:
        raise Exception(
            "RABBITMQ_URL não configurada no .env"
        )

    params = pika.URLParameters(
        RABBITMQ_URL
    )

    return pika.BlockingConnection(
        params
    )


def publish_job(job_id: str):
    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    message = {
        "job_id": job_id
    }

    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()