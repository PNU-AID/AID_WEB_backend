from backend.database import db
from backend.scheme import UserCreate
from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

# user에 관한 crud 기능 구현


def create_user(user: UserCreate):  # user create를 상속받는 create기능 구현
    """유저 생성"""
    user = jsonable_encoder(user)
    # user password hashing
    # nick_name valid check
    db.user.insert_one(user)


def read_all_user():
    """모든 유저 읽기"""
    all_users = db.user.find()  # find 함수를 통해 모든 유저를 읽어온다.
    return all_users


def read_user(user_nick_name: str):  # user읽기
    """user_nick_name에 해당하는 정보 반환"""
    user = db.user.find_one({"nick_name": user_nick_name})  # find_one함수를 통해 닉네임과 이리하는 유저를 읽어온다.
    return user


def read_all_is_pass_email(is_pass: bool):
    cursor = db["submit"].find({"is_pass": is_pass}, {"email": 1})
    email_list = [result["email"] for result in cursor]
    return email_list


def update_user(change_info):  # user 업데이트
    change_info = jsonable_encoder(change_info)
    user_id = change_info.pop("_id")
    user_id = ObjectId(user_id)

    res = db.user.find_one_and_update(
        {"_id": user_id}, {"$set": {**change_info}}
    )  # find_one_and_update함수로 닉네임과 change_info를 넘겨준다.
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")  # 404 errror 생성코드(일치하는 유저가 없을시)


def delete_user(user_id: str):  # user 삭제
    user_id = ObjectId(user_id)
    res = db.user.find_one_and_delete({"_id": user_id})
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
