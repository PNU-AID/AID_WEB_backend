from backend.database import db_manager
from backend.scheme import UserCreate
from fastapi import APIRouter

router = APIRouter()  # auth 라우터를 위한 api router 선언부

# author에 대한 api를 담은 코드


@router.post("/signup")
def create_user(user: UserCreate):
    # 유저 password hashing
    db_manager.db.test.insert_one({"test": "test"})


@router.post("/login")
def login(user: UserCreate):
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


@router.delete("/signout")
def signout(user: UserCreate):
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
