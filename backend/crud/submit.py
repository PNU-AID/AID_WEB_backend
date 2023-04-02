from backend.database import db


def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit():
    # TODO
    pass


def read_submit(_id: str):
    # TODO
    pass
