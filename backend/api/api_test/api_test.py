from crud import (
    create_user,
    delete_user,
    read_all_user,
    read_user,
    update_user,
)
from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse, ORJSONResponse
from scheme import UserCreate, UserOut, UserUpdate
from utils import make_message

router = APIRouter()


@router.post("/create")
def create(
    user: UserCreate = Body(
        example={
            "nick_name": "test",
            "password": "1234",
            "email": "test@email.com",
        }
    )
):
    """유저 생성

    - nick_name
    - password
    - email

    """
    try:
        create_user(user)
        # https://stackoverflow.com/questions/71467630/fastapi-issues-with-mongodb-typeerror-objectid-object-is-not-iterable?noredirect=1&lq=1

    except Exception:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=make_message("서버 에러"),
        )
    return JSONResponse(content=make_message("Sing Up Successful"), status_code=status.HTTP_201_CREATED)


@router.get("/read", response_model=UserOut, status_code=status.HTTP_200_OK)
def read_one(nick_name: str):
    """nick_name에 해당하는 유저 정보 반환"""
    user = read_user(nick_name)
    return user


@router.get("/read/all", response_model=list[UserOut], status_code=status.HTTP_200_OK)
def read_all():
    """모든 유저 정보 반환"""
    all_user = read_all_user()
    # cusor가 반환되므로 list로 변환이 필요
    return list(all_user)


@router.put("/update")
def update(user_info: UserUpdate):
    update_user(user_info)
    return ORJSONResponse(content=make_message("수정 완료"), status_code=status.HTTP_200_OK)


@router.delete("/delete")
def delete(
    user_id: str,
):
    delete_user(user_id)
    return ORJSONResponse(content=make_message("삭제 완료"), status_code=status.HTTP_200_OK)
