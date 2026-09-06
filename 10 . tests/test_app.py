from fastapi.testclient import TestClient
from ai_interview_project.main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    