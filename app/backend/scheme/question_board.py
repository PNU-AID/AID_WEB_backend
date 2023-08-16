from datetime import datetime

from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)


class QuestionIn(QuestionBase):
    pass


class QuestionInDB(QuestionBase):
    created_time: datetime
    comment_ids: list


class QuestionOut(QuestionBase):
    created_time: datetime
    content: str
    comments: list


class CommentIn(BaseModel):
    question_id: str = Field(...)
    content: str = Field(...)


class CommentInDB(BaseModel):
    created_time: datetime
