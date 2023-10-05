from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.core import settings
from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)
from app.crud.user import create_user_in_db, read_user_in_db
from app.schemas.user import UserAuth, UserOut

router = APIRouter()


async def authentication_user(user_auth: UserAuth):
    """
    valid check user

    return User or False
    """
    user = await read_user_in_db(user_auth.email)
    if user is None:
        return False
    if not verify_password(user_auth.password, user.password):
        return False
    return user


@router.post("/signup", response_model=UserOut)
async def create_user(user_auth: UserAuth):
    """create a new user"""
    user = await read_user_in_db(user_auth.email)
    if user is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with that email already exists")

    # TODO
    # email validation

    hashed_pwd = get_password_hash(user_auth.password)
    user = create_user_in_db(email=user_auth.email, password=hashed_pwd)
    return user


@router.post("/login")
async def login(user_auth: UserAuth):
    user = await authentication_user(user_auth)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expire)

    expires = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    # refresh_token_expire = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(data={"sub": user.email})

    header = {"Authorization": f"Bearer {access_token}"}
    # TODO
    # content 수정
    response = JSONResponse(content={"status": "success"}, headers=header)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        expires=expires.strftime("%a, %d %b %Y %H:%M:%S GMT"),
    )

    return response
