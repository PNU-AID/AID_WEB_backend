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
    valid = True
    if valid:
        create_user(user)
    else:
        return {"message": "signup fail"}

    return {"message": "signup success"}


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
