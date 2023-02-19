from bson import ObjectId
from database import db
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from scheme import UserCreate


def create_user(user: UserCreate):
    user = jsonable_encoder(user)
    # user password hashing
    # nick_name valid check
    db.user.insert_one(user)


def read_all_user():
    all_users = db.user.find()
    return all_users


def read_user(user_nick_name: str):
    user = db.user.find_one({"nick_name": user_nick_name})
    return user


def update_user(user_id: str, change_info):
    user_id = ObjectId(user_id)
    user = db.user.find_one({"_id": user_id})

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    change_info = jsonable_encoder(change_info)
    result = db.user.update_one({"_id": user_id}, {"$set": {**change_info}})

    # Check if the update was successful
    if result.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to update user name")
