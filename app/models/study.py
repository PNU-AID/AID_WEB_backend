from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, Field, HttpUrl
from pydantic.functional_validators import model_validator

from .user import User


class CommentForm(BaseModel):
    writer: Link[User]
    content: str


class statusEnum(str, Enum):
    """상태를 나타내는 enumerate datatype

    closed: 스터디가 종료됨
    open: 스터디 모집중
    canceled: 인원 부족, 팀장에 의한 취소 등으로 스터디가 종료됨
    """

    closed = "closed"
    open = "opened"
    canceled = "canceled"


class Study(Document):
    """User DB representation"""

    owner: Link[User]
    title: str
    content: str
    participants: List[Link[User]] = []
    participants_wait: List[Link[User]] = []
    comments: Optional[List[CommentForm]] = None
    max_participants: int = Field(gt=1)
    cur_participants: int = 0
    likes: int = Field(default=0)
    url: Optional[HttpUrl] = None
    created_time: datetime = Field(default_factory=datetime.now)
    expire_time: datetime
    status: statusEnum = statusEnum.open

    @model_validator(mode="after")
    def check_expire_gt_than_created(self) -> "Study":
        if self.created_time >= self.expire_time:
            raise ValueError("expire_time must be greater than created_time")
        return self

    async def create(self, *args, **kwargs):
        self.participants.append(self.owner)
        self.cur_participants = len(self.participants)
        self._validate_after_creation = True
        await super().create(*args, **kwargs)

    class Settings:
        name = "study"
