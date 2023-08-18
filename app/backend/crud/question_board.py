from backend.database import db_manager
from backend.scheme.question_board import CommentIn
from bson import ObjectId


def create_question(question_data: dict):
    db_manager.db.question.insert_one(question_data)


def create_comment(comment_data: CommentIn):
    comment_input = db_manager.db.comment.insert_one(comment_data.dict())
    return str(comment_input.inserted_id)


def insert_comment_in_question(question_id: str, comment_id: str):
    db_manager.db.question.update_one({"_id": ObjectId(question_id)}, {"$push": {"comment_ids": comment_id}})


def read_question(question_id: str) -> dict:
    question_output = db_manager.db.question.find_one({"_id": ObjectId(question_id)})
    return question_output


def read_all_question() -> list:
    question_outputs = db_manager.db.question.find()
    result = []
    for output in question_outputs:
        output["_id"] = str(output["_id"])
        result.append(output)
    return result


def get_comments(question_id: str) -> list:
    results = db_manager.db.comment.find({"question_id": question_id})
    result = []
    for info in results:
        result.append(info["content"])
    return result


# TODO
# update_question


def delete_question(question_id: str):
    db_manager.db.question.delete_one({"_id": ObjectId(question_id)})
    db_manager.db.comment.delete_many({"question_id": question_id})


def delete_comment(question_id: str, comment_id: str):
    db_manager.db.comment.delete_one({"_id": ObjectId(comment_id)})
    db_manager.db.question.update_one({"_id": ObjectId(question_id)}, {"$pull": {"comment_ids": comment_id}})
