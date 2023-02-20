import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

test_id = None


@pytest.mark.order(1)
def test_create_user():
    response = client.post(
        url="api/test/create",
        json={"nick_name": "테스트", "password": "1234qwer", "email": "테스트1234@email.com"},
    )

    assert response.status_code == 201


@pytest.mark.order(2)
def test_read_user_1():
    global test_id
    response = client.get("api/test/read", params={"nick_name": "테스트"})
    assert response.status_code == 200

    res = response.json()
    test_id = res.pop("_id")
    assert res == {
        "nick_name": "테스트",
        "email": "테스트1234@email.com",
        "is_club_member": False,
        "admin": False,
    }


@pytest.mark.order(3)
def test_read_all_user():
    response = client.get("api/test/read/all")
    assert response.status_code == 200
    assert type(response.json()) == list


@pytest.mark.order(4)
def test_update_user():
    response = client.put(
        "api/test/update",
        json={
            "_id": test_id,
            "nick_name": "수정",
            "password": "패스워드",
            "email": "테스트이메일@email.com",
        },
    )
    assert response.status_code == 200


@pytest.mark.order(5)
def test_read_user_2():
    response = client.get("api/test/read", params={"nick_name": "수정"})
    assert response.status_code == 200

    res = response.json()
    res.pop("_id")
    assert res == {
        "nick_name": "수정",
        "email": "테스트이메일@email.com",
        "is_club_member": False,
        "admin": False,
    }


@pytest.mark.order(6)
def test_delete_user():
    # https://github.com/tiangolo/fastapi/issues/5649
    response = client.delete(f"api/test/delete?user_id={test_id}")
    assert response.status_code == 200
