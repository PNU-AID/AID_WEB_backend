from datetime import datetime
from typing import List, Optional

from beanie import Link, PydanticObjectId
from pydantic import BaseModel

from app.models.study import StudyStatus
from app.models.user import User
from app.schemas.user import UserOut


# 스터디 출력용 field
class StudyCommentOut(BaseModel):
    """스터디 댓글(작성자, 내용)"""

    writer: UserOut
    content: str


class LikesOut(BaseModel):
    """스터디 좋아요 정보(좋아요 수만 출력)"""

    likeCount: int


class StudyUserOutput(BaseModel):
    """스터디 관련 User 출력(id, email, nick_name)"""

    id: PydanticObjectId
    email: str
    nick_name: str


# 스터디 입,출력 schema
class StudyCreate(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_time: datetime
    url: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "test_title",
                    "content": "test_content",
                    "max_participants": 10,
                    "expire_time": str(datetime.now()),
                    "url": "",
                }
            ]
        }
    }


class StudyUpdate(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_time: datetime
    owner_id: PydanticObjectId
    status: StudyStatus
    url: Optional[str]


class StudyComment(BaseModel):
    comment: str


class StudyOutputSimple(BaseModel):
    id: PydanticObjectId
    owner: Link[User]
    title: str
    content: str
    comments: List[StudyCommentOut]
    max_participants: int
    cur_participants: int
    likes: LikesOut
    url: Optional[str]
    created_time: datetime
    expire_time: datetime
    status: StudyStatus


class StudyOutput(StudyOutputSimple):
    owner: StudyUserOutput
    participants: List[StudyUserOutput]
    participants_wait: List[StudyUserOutput]
