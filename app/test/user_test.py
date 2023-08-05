from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# TODO
# make api test function


def test_sign_up():
    response = client.post("/signup", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 404
    assert response.json() == {"email": "test@example.com", "password": "password"}
