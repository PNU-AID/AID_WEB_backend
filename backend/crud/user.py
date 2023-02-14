from database import db
from fastapi.encoders import jsonable_encoder
from scheme import UserCreate


def create_user(user: UserCreate):
    user = jsonable_encoder(user)
    new_user = db.user.insert_one(user)
    db_user = db.user.find_one({"_id": new_user.inserted_id})
    return db_user


def read_all_user():
    all_users = db.user.find()
    return all_users


def read_user(user_nick_name: str):
    user = db.user.find_one({"nick_name": user_nick_name})
    return user
