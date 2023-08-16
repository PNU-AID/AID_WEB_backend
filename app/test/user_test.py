from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# TODO
# make api test function


def test_sign_up():
    response = client.post(
        "/create",
        json={
            "name": "asdf",
            "email": "EmailStr",
            "student_id": "asdf",
            "phone_number": "str",
            "motivation": "str",
            "github": "foo",
            "blog": "bar",
            "ai_exp": "foo",
            "personal_info_agree": "true",
        },
    )

    assert response.status_code == 201
    assert response.json() == {"id": "Foo"}
