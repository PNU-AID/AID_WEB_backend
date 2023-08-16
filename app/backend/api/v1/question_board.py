from datetime import datetime

from backend.crud.question_board import (
    create_comment,
    create_question,
    delete_comment,
    delete_question,
    get_comments,
    insert_comment_in_question,
    read_all_question,
    read_question,
)
from backend.scheme.question_board import (
    CommentIn,
    QuestionIn,
    QuestionOut,
)
from fastapi import APIRouter, Query

# submit에 관한 api를 담은 코드

router = APIRouter()  # submit ROUTER 를 선언해준다.


@router.post("/create_question")
def upload_question(question: QuestionIn):
    question = question.model_dump()
    question["created_time"] = datetime.now()
    question["comment_ids"] = []
    create_question(question)
    return {"message": "succeeded"}


@router.post("/create_comment")
def upload_comment(comment: CommentIn):
    comment_id = create_comment(comment)
    insert_comment_in_question(comment.question_id, comment_id)
    return {"message": "succeeded"}


@router.get("/get_question", response_model=QuestionOut)
def get_my_question(question_id: str = Query()):
    question = read_question(question_id)
    del question["comment_ids"]
    comments = get_comments(question_id)
    question["comments"] = comments
    return question


@router.get("/get_all_question")
def get_all_question():
    question = read_all_question()
    return question


@router.delete("/delete_question")
def cancel_question(question_id: str):
    delete_question(question_id)
    return {"message": "deleted succeeded"}


@router.delete("/delete_comment")
def cancel_comment(comment_id: str, question_id: str):
    delete_comment(question_id, comment_id)
    return {"message": "deleted succeeded"}
