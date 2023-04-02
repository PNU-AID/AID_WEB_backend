from backend.database import db


def create_submit(data: dict):
    db["submit"].insert_one(data)


def read_all_submit(data):
    pass


def read_submit(data):
    pass
