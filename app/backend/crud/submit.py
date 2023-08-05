from backend.database import db_manager
from backend.scheme.submit import SubmitForm
from bson import ObjectId


def create_submit(submit_data: SubmitForm) -> str:
    submit_input = db_manager.db.submit.insert_one(submit_data.dict())
    return str(submit_input.inserted_id)


def read_submit(submit_id: str) -> dict:
    submit = db_manager.db.submit.find_one({"_id": ObjectId(submit_id)})
    return submit


def update_submit(submit_id: str, submit_data: SubmitForm):
    db_manager.db.submit.update_one({"_id": ObjectId(submit_id)}, {"$set": submit_data.dict()})


def delete_submit(submit_id: str):
    # TODO
    # make this part
    pass
    


def read_all_submit():
    pass
