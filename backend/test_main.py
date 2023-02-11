# To solve module not found error # noqa
import sys

from fastapi.testclient import TestClient

from .main import app

sys.path.append("./")

client = TestClient(app)


def test_get():
    response = client.get("api/test/get")
    assert response.status_code == 200
    assert response.json() == {"message": "test"}


def test_create_user():
    response = client.post(
        url="api/test/create",
        json={"nick_name": "test", "password": "1234", "email": "test@email.com"},
    )

    assert response.status_code == 201
    assert response.json() == {
        "nick_name": "test",
        "email": "test@email.com",
        "is_club_member": False,
        "admin": False,
    }
