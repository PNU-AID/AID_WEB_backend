from fastapi import APIRouter, Depends
from fastapi.responses import Response

from app.core.security import get_current_user
from app.schemas.user import UserOut

router = APIRouter()

# TODO
# middleware 추가


@router.get("/read", response_model=UserOut)
def read_user(response: Response, user_and_token: dict = Depends(get_current_user)):
    user = user_and_token["user"]
    access_token = user_and_token["token"]

    response.headers["Authorization"] = f"Bearer {access_token}"

    return user


@router.put("/update")
def update_user():
    pass


@router.delete("/delete")
def delete_user():
    pass
