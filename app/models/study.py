from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, Field
from pydantic.functional_validators import model_validator

from .user import User


class CommentForm(BaseModel):
    writer: Link[User]
    content: str


class Likes(BaseModel):
    likeCount: int = 0
    likeID: List[Link[User]] = []


class StudyStatus(str, Enum):
    """상태를 나타내는 enumerate datatype

    closed: 스터디가 종료됨
    open: 스터디 모집중
    canceled: 인원 부족(시간 초과), 팀장에 의한 취소 등으로 스터디가 종료됨
    """

    closed = "closed"
    open = "opened"
    canceled = "canceled"


class Study(Document):
    """User DB representation"""

    # TODO : replace() override후 cur_participants 업데이트하기

    owner: Link[User]
    title: str
    content: str
    participants: List[Link[User]] = Field(unique=True, default=[])
    participants_wait: List[Link[User]] = Field(unique=True, default=[])
    comments: List[CommentForm] = []
    max_participants: int = Field(gt=1)
    cur_participants: int = 0
    likes: Likes = Likes()
    url: Optional[str] = None
    created_time: datetime = Field(default_factory=datetime.now)
    expire_time: datetime
    status: StudyStatus = StudyStatus.open

    @model_validator(mode="after")
    def check_expire_gt_than_created(self) -> "Study":
        if self.created_time >= self.expire_time:
            raise ValueError("expire_time must be greater than created_time")
        return self

    async def create(self, *args, **kwargs):
        self.participants.append(self.owner)
        self.cur_participants = len(self.participants)
        await super().create(*args, **kwargs)

    class Settings:
        name = "study"
