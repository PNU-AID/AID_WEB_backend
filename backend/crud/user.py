from bson import ObjectId
from database import db
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from scheme import UserCreate


def create_user(user: UserCreate):
    """유저 생성"""
    user = jsonable_encoder(user)
    # user password hashing
    # nick_name valid check
    db.user.insert_one(user)


def read_all_user():
    """모든 유저 읽기"""
    all_users = db.user.find()
    return all_users


def read_user(user_nick_name: str):
    """user_nick_name에 해당하는 정보 반환"""
    user = db.user.find_one({"nick_name": user_nick_name})
    return user


def update_user(change_info):
    change_info = jsonable_encoder(change_info)
    user_id = change_info.pop("_id")
    user_id = ObjectId(user_id)

    res = db.user.find_one_and_update({"_id": user_id}, {"$set": {**change_info}})
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")


def delete_user(user_id: str):
    user_id = ObjectId(user_id)
    res = db.user.find_one_and_delete({"_id": user_id})
    if res is None:
        raise HTTPException(status_code=404, detail="User not found")
