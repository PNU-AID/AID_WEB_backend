from typing import Union

from backend.core.security import get_password_hash
from backend.database import db_manager
from backend.scheme.user import UserOutDB, UserSignUp
from pydantic import EmailStr


def create_user(user: UserSignUp, is_admin=False) -> None:
    # hash
    hash_password = get_password_hash(user.password)
    user_dict = user.dict()
    del user_dict["password"]
    if is_admin:
        user_dict["is_admin"] = True
    else:
        user_dict["is_admin"] = False
    user_dict["hash_password"] = hash_password
    # inser to db
    db_manager.db.user.insert_one(user_dict)


def read_all_user():
    pass


def read_user(email: EmailStr) -> Union[UserOutDB, None]:
    user_info = db_manager.db.user.find_one({"email": email})
    if user_info is None:
        return None
    return UserOutDB(**user_info)


def read_all_is_pass_email(is_pass: bool):
    pass


def update_user(change_info):  # user 업데이트
    pass


def delete_user(user_id: str):  # user 삭제
    pass
