from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_get():
    response = client.get("api/test/get")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}
