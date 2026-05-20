from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import uuid
import os

from app.db.database import SessionLocal
from app.db.models import AnalysisJob
from app.services.rabbitmq_service import publish_job

router = APIRouter()


@router.post("/upload")
async def upload(
        file: UploadFile = File(...)
):

    db = SessionLocal()

    # VALIDAÇÃO DE EXTENSÃO
    allowed_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".pdf"
    ]

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed_extensions:

        return {
            "error":
                "invalid_file_type"
        }

    job_id = str(uuid.uuid4())

    content = await file.read()

    os.makedirs(
        "storage",
        exist_ok=True
    )

    filepath = (
        f"storage/"
        f"{job_id}_{file.filename}"
    )

    with open(
            filepath,
            "wb"
    ) as f:

        f.write(content)

    job = AnalysisJob(
        id=job_id,
        filename=filepath,
        status="RECEIVED"
    )

    db.add(job)

    db.commit()

    publish_job(job_id)
    
    db.close()

    return {
        "job_id": job_id,
        "status": "RECEIVED"
    }