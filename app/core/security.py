from datetime import datetime, timedelta
from typing import Annotated, Union

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security.http import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from app.core import settings
from app.crud.user import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
get_bearer_token = HTTPBearer(auto_error=False)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_access_token(auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]) -> str:
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token is missing or unknown")
    token = auth.credentials
    return token


async def get_current_user(
    refresh_token: Annotated[Union[str, None], Cookie()], access_token: Annotated[str, Depends(get_access_token)]
):
    credential_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        # 시간 만료 에러
        print("expire")
        if refresh_token is None:
            raise credential_err
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, settings.ALGORITHM)

    except JWTError:
        # 모든 jwt 에러
        raise credential_err

    email: str = payload.get("sub")
    if email is None:
        raise credential_err

    user = await get_user_by_email(email)
    if user is None:
        raise credential_err

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expire)
    return {"user": user, "token": access_token}
