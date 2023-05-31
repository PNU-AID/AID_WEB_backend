from fastapi.testclient import TestClient

from app.backend.main import app


def test_hompage():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.template.name == "home.html"
    assert "request" in response.context
