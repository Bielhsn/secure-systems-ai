from fastapi import APIRouter
from app.db.database import SessionLocal
from app.db.models import AnalysisJob

router = APIRouter()


@router.get("/status/{job_id}")
def get_status(job_id: str):

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
            "job_id": job.id,
            "status": job.status,
            "result": job.result,
            "report_path":
                job.report_path,
            "error_message":
                job.error_message
        }

    return {
        "job_id": job.id,
        "status": job.status,
        "result": job.result,
        "error_message":
            job.error_message
    }