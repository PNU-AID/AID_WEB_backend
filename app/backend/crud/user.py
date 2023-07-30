from datetime import datetime

from backend.core import hasher
from backend.core.utils import get_random_name
from backend.database import db_manager
from backend.scheme import UserCreate
from fastapi.encoders import jsonable_encoder


def create_user(user: UserCreate, is_admin=False):
    # json변환
    user = jsonable_encoder(user)
    # hash
    user["password"] = hasher.get_password_hash(user["password"])

    # initialize
    user["created_time"] = datetime.now()
    if is_admin:
        user["is_admin"] = True
    else:
        user["is_admin"] = False

    user["is_member"] = False
    user["is_active"] = False
    user["submit"] = None
    user["articles"] = []
    user["nick_name"] = get_random_name(12)

    # inser to db
    db_manager.db.user.insert_one({**user})


def read_all_user():
    pass


def read_user(nick_name: str):
    db_manager.db.user.find_one({"nick_name": nick_name})


def read_all_is_pass_email(is_pass: bool):
    pass


def update_user(change_info):  # user 업데이트
    pass


def delete_user(user_id: str):  # user 삭제
    pass
