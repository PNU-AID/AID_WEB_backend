from datetime import datetime

from backend.core.utils import ObjectIdStr, StrObjectId
from pydantic import BaseModel, Field

# 위 코드는 Pydantic을 사용하여 MongoDB에서 사용될 "User 데이터 모델과 관련된 클래스"들을 정의하고 있다.


class QuestionBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)
    comments: list = []


class QuestionIn(QuestionBase):
    created_time: datetime = Field(default_factory=datetime.now)


class QuestionOut(QuestionBase):
    id: ObjectIdStr = Field(alias="_id")
    created_time: datetime

    class Config:
        arbitrary_types_allowed = True


class CommentIn(BaseModel):
    question_id: StrObjectId = Field(...)
    created_time: datetime = Field(default_factory=datetime.now)
    content: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
