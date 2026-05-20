import json
import logging

import pika

from app.db.database import SessionLocal
from app.db.models import AnalysisJob

from app.services.rabbitmq_service import (
    get_connection,
    QUEUE_NAME
)

from app.services.vision_service import (
    analyze_diagram_image
)

from app.services.report_service import (
    generate_report_pdf
)


logging.basicConfig(
    level=logging.INFO
)


def process_job(job_id: str):

    db = SessionLocal()

    job = (
        db.query(AnalysisJob)
        .filter(
            AnalysisJob.id == job_id
        )
        .first()
    )

    if not job:
        logging.error(
            f"Job não encontrado: {job_id}"
        )
        db.close()
        return

    try:
        logging.info(
            f"Processando job {job.id}"
        )

        job.status = "PROCESSING"
        db.commit()

        result = analyze_diagram_image(
            job.filename
        )

        report_path = generate_report_pdf(
            job.id,
            result
        )

        job.extracted_text = (
            "multimodal_analysis"
        )

        job.result = json.dumps(
            result,
            ensure_ascii=False
        )

        job.report_path = report_path
        job.status = "DONE"
        job.error_message = None

        db.commit()

        logging.info(
            f"Job concluído: {job.id}"
        )

    except Exception as e:

        job.status = "ERROR"
        job.error_message = str(e)

        db.commit()

        logging.error(
            f"Erro ao processar job {job.id}: {e}"
        )

    finally:
        db.close()


def callback(
        ch,
        method,
        properties,
        body
):

    try:
        message = json.loads(
            body.decode("utf-8")
        )

        job_id = message.get(
            "job_id"
        )

        if not job_id:
            raise Exception(
                "Mensagem sem job_id"
            )

        process_job(job_id)

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception as e:

        logging.error(
            f"Erro no callback RabbitMQ: {e}"
        )

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=False
        )


def run_worker():

    logging.info(
        "IA Worker iniciado com RabbitMQ..."
    )

    connection = get_connection()

    channel = connection.channel()

    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )

    channel.basic_qos(
        prefetch_count=1
    )

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    logging.info(
        "Aguardando mensagens..."
    )

    channel.start_consuming()


if __name__ == "__main__":
    run_worker()