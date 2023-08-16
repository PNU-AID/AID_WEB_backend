from backend.crud.question_board import (
    create_comment,
    create_question,
    delete_comment,
    delete_question,
    insert_comment_in_question,
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
    create_question(question)
    return {"message": "succeeded"}


@router.post("/create_comment")
def upload_comment(comment: CommentIn, question_id: str):
    comment_id = create_comment(comment)
    insert_comment_in_question(question_id, comment_id)


@router.get("/get_question", response_model=QuestionOut)
def get_my_question(question_id: str = Query()):
    question = read_question(question_id)
    return question


@router.delete("/delete_question")
def cancel_question(question_id: str):
    delete_question(question_id)
    return {"msg": "deleted succeeded"}


@router.delete("/delete_comment")
def cancel_comment(comment_id: str):
    delete_comment(comment_id)
