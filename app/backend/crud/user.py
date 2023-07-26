from backend.database import db_manager
from backend.scheme import UserCreate


def create_user(user: UserCreate):  # user create를 상속받는 create기능 구현
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
