from bson import ObjectId

from backend.database import db


def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit():
    return db["submit"].find()


def read_submit(_id: str):
    return db["submit"].find_one({"_id": ObjectId(_id)})


def update_is_pass(_id: str, is_pass):
    # one = db["submit"].find_one({"_id": ObjectId(_id)})
    # one.is_pass = is_pass

    db["submit"].find_one({"_id": ObjectId(_id)}).updateOne({"submit"})
