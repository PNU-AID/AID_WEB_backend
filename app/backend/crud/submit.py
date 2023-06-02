from backend.database import db
from bson import ObjectId


def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit():
    return db["submit"].find()


def get_count():
    return db["submit"].count_documents({})


def read_submit(_id: str):
    return db["submit"].find_one({"_id": ObjectId(_id)})


def update_is_pass(_id: str, is_pass: bool):
    query = {"_id": ObjectId(_id)}
    new_value = {"$set": {"is_pass": is_pass}}

    db["submit"].update_one(query, new_value)
