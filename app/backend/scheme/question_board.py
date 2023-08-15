from datetime import datetime

from backend.core.utils import ObjectIdStr
from pydantic import BaseModel, Field

# 위 코드는 Pydantic을 사용하여 MongoDB에서 사용될 "User 데이터 모델과 관련된 클래스"들을 정의하고 있다.


class QuestionBase(BaseModel):
    title: str = Field(...)
    content: str = Field(...)


class QuestionIn(QuestionBase):
    created_time: datetime = Field(default_factory=datetime.now)
    comments: list = []


class QuestionOut(QuestionBase):
    id: ObjectIdStr = Field(alias="_id")
    created_time: datetime
    comments: list = []

    class Config:
        arbitrary_types_allowed = True
