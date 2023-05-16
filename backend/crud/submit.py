from bson import ObjectId

from backend.database import db


def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit():
    return db["submit"].find()


def get_count():
    return db["submit"].count_documents({})


def read_submit(_id: str):
    return db["submit"].find_one({"_id": ObjectId(_id)})
