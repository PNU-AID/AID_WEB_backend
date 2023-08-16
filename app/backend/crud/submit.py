from backend.database import db_manager
from bson import ObjectId


def create_submit(submit_data: dict) -> str:
    """지원서 저장

    Args:
        submit_data (dict)

    Returns:
        str: str type object id
    """
    result = db_manager.db.submit.insert_one(submit_data)
    return str(result.inserted_id)


def read_submit(submit_id: str) -> dict | None:
    """지원서 가져오기

    Args:
        submit_id (str)

    Returns:
        dict: submit form 내용
    """
    submit = db_manager.db.submit.find_one({"_id": ObjectId(submit_id)})
    return submit


def update_submit(submit_id: str, submit_data: dict):
    """지원서 수정

    Args:
        submit_id (str)
        submit_data (dict)
    """
    # 없는 id 입력될 시 에러
    db_manager.db.submit.update_one({"_id": ObjectId(submit_id)}, {"$set": submit_data})


def delete_submit(submit_id: str):
    # 없는 id 입력될 시 에러
    db_manager.db.submit.delete_one({"_id": ObjectId(submit_id)})


def read_all_submit():
    pass
