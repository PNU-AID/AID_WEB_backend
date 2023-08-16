from backend.database import db_manager
from backend.scheme.question_board import CommentIn, QuestionIn
from bson import ObjectId


def create_question(question_data: QuestionIn):
    db_manager.db.question.insert_one(question_data.dict())


def create_comment(comment_data: CommentIn):
    comment_input = db_manager.db.comment.insert_one(comment_data.dict())
    return str(comment_input.inserted_id)


def insert_comment_in_question(question_id: str, comment_id: str):
    # question = db_manager.db.question.find_one({"_id": ObjectId(question_id)})
    db_manager.db.question.update_one({"_id": question_id}, {"$push": {"comments": ObjectId(comment_id)}})


def read_question(question_id: str) -> dict:
    question_output = db_manager.db.question.find_one({"_id": ObjectId(question_id)})
    return question_output


# TODO
# update_question


def delete_question(question_id: str):
    db_manager.db.question.delete_one({"_id": ObjectId(question_id)})


def delete_comment(comment_id: str):
    db_manager.db.question.comment.delete_one({"_id": ObjectId(comment_id)})
