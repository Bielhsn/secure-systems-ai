import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph
)

from reportlab.lib import styles


def generate_report_pdf(
        job_id: str,
        result: dict
):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    filepath = (
        f"reports/"
        f"{job_id}_report.pdf"
    )

    doc = SimpleDocTemplate(
        filepath
    )

    style = styles.getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Technical Architecture Analysis Report",
        style["Title"]
    )

    content.append(title)
    content.append(
        Spacer(1, 20)
    )

    score = Paragraph(
        (
            f"<b>Architecture Score:</b> "
            f"{result.get('architecture_score', 0)}/10"
        ),
        style["BodyText"]
    )

    content.append(score)
    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "Components Identified",
            style["Heading2"]
        )
    )

    for item in result.get(
            "components", []
    ):
        content.append(
            Paragraph(
                f"• {item}",
                style["BodyText"]
            )
        )

    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "Architectural Risks",
            style["Heading2"]
        )
    )

    for item in result.get(
            "risks", []
    ):
        content.append(
            Paragraph(
                f"• {item}",
                style["BodyText"]
            )
        )

    content.append(
        Spacer(1, 10)
    )

    content.append(
        Paragraph(
            "Recommendations",
            style["Heading2"]
        )
    )

    for item in result.get(
            "recommendations", []
    ):
        content.append(
            Paragraph(
                f"• {item}",
                style["BodyText"]
            )
        )

    doc.build(content)

    return filepath