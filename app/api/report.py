import os

from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.db.database import SessionLocal
from app.db.models import AnalysisJob


router = APIRouter()


@router.get("/report/{job_id}")
def download_report(job_id: str):

    db = SessionLocal()

    job = (
        db.query(AnalysisJob)
        .filter(
            AnalysisJob.id == job_id
        )
        .first()
    )

    db.close()

    if not job:
        return {
            "error": "job_not_found"
        }

    if not job.report_path:
        return {
            "error": "report_not_generated"
        }

    if not os.path.exists(job.report_path):
        return {
            "error": "report_file_not_found"
        }

    return FileResponse(
        path=job.report_path,
        media_type="application/pdf",
        filename=f"{job_id}_report.pdf"
    )