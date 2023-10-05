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
from app.schemas.auth import Token

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


def get_access_token_header(auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)]):
    if auth is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token is missing or unknown")
    else:
        access_token = auth.credentials
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
            if payload.get("sub") is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token is missing or unknown"
                )
        except ExpiredSignatureError:
            pass
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token is missing or unknown")


async def get_token(
    refresh_token: Annotated[Union[str, None], Cookie()],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(get_bearer_token)],
) -> Token:
    credential_err = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    access_token = auth.credentials
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        # 시간 만료 에러
        if refresh_token is None:
            raise credential_err
        payload = jwt.decode(refresh_token, settings.REFRESH_SECRET_KEY, settings.ALGORITHM)

    except JWTError:
        # 모든 jwt 에러
        raise credential_err

    email: str = payload.get("sub")
    if email is None:
        raise credential_err

    access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": email}, expires_delta=access_token_expire)

    # pydantic BaseModel class용도로 사용하는 경우 반드시 키워드 인자값으로 사용해야 함
    token = Token(email=email, access_token=access_token)
    return token
