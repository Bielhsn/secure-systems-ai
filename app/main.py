from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.status import router as status_router
from app.api.report import router as report_router

from app.db.init_db import create_tables


app = FastAPI(
    title="Secure Systems AI"
)

create_tables()

app.include_router(upload_router)
app.include_router(status_router)
app.include_router(report_router)


@app.get("/")
def health():
    return {
        "status": "running"
    }