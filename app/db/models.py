from sqlalchemy import (
    Column,
    String,
    Text
)

from app.db.database import Base


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(
        String,
        primary_key=True,
        index=True
    )

    filename = Column(String)

    status = Column(String)

    extracted_text = Column(
        Text,
        nullable=True
    )

    result = Column(
        Text,
        nullable=True
    )

    report_path = Column(
        String,
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )