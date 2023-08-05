from datetime import timedelta
from typing import Union

from backend.core import settings
from backend.core.security import create_access_token, verify_password
from backend.core.utils import make_message
from backend.crud.user import create_user, read_user
from backend.scheme.user import (
    UserLogIn,
    UserOut,
    UserOutDB,
    UserSignUp,
)
from fastapi import APIRouter, HTTPException, Response, status

router = APIRouter()  # auth 라우터를 위한 api router 선언부


def authenticate_user(user: UserLogIn) -> Union[UserOutDB, None]:
    user_info = read_user(user.email)

    if user_info is None:
        return None
    if not verify_password(user.password, user_info.hash_password):
        return None

    return user_info


@router.post("/signup")
def signup(user: UserSignUp):
    user_check = read_user(user.email)
    if user_check is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exist")

    create_user(user)

    return make_message("user created")


@router.post("/login", response_model=UserOut)
def login(response: Response, user: UserLogIn):
    user_info = authenticate_user(user)
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    response.set_cookie(key="Authorization", value=access_token, httponly=True, expires=1800)

    return user_info


@router.post("/logout")
def logout(user: UserLogIn):
    # 유저 password hashing

    return user


@router.delete("/withdraw")
def withdraw_account(user):
    # 유저 password hashing
    return user


@router.put("/modify")
def modify(user):
    # 유저 password hashing
    return user


@router.get("/get_user")
def get_user_info(user):
    # 유저 password hashing
    return user
