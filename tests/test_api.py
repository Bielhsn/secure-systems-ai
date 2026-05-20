from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_status_job_not_found():
    response = client.get(
        "/status/job-inexistente"
    )

    assert response.status_code == 200
    assert response.json()["error"] == "job_not_found"


def test_invalid_file_upload():
    file_content = b"arquivo invalido"

    response = client.post(
        "/upload",
        files={
            "file": (
                "teste.txt",
                file_content,
                "text/plain"
            )
        }
    )

    assert response.status_code == 200
    assert response.json()["error"] == "invalid_file_type"