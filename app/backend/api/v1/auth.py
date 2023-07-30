from backend.core.utils import EmailValidator
from backend.crud import create_user
from backend.scheme import UserCreate, UserLogIn
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()  # auth 라우터를 위한 api router 선언부


@router.post("/signup")
def signup(user: UserCreate):
    # TODO
    # valid user email
    # valid = True

    valid = EmailValidator(user.email)

    if valid:  # email 형식에 맞으면
        create_user(user)  # json형태로 변경한 후에 hashing한 후 미리 정의한 dbmanager를 이용해 db로 user 저장.
    else:  # email 형식에 맞지 않으면
        return {"message": "signup fail"}  # 실패 json object message 반환

    return {"message": "signup success"}  # 성공 json object message 반환


@router.post("/login")
def login(user: UserLogIn):
    """login 하는 api

    Args:
        user (UserCreate): _description_

    Returns:
        _type_: _description_
    """

    return user


@router.post("/logout")
def logout(user: UserCreate):
    # 유저 password hashing

    return user


@router.delete("/withdraw")
def withdraw_account(user: UserCreate):
    # 유저 password hashing
    return user


@router.put("/modify")
def modify(user: UserCreate):
    # 유저 password hashing
    return user


@router.get("/get_user")
def get_user_info(user: UserCreate):
    # 유저 password hashing
    return user
