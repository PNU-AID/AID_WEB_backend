from datetime import datetime
from typing import List, Optional

from beanie import Link, PydanticObjectId
from pydantic import BaseModel

from app.models.study import StudyStatus
from app.models.user import User
from app.schemas.user import UserOut


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
    class StudyCommentOut(BaseModel):
        writer: UserOut
        content: str

    class LikesOut(BaseModel):
        likeCount: int

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
    class StudyUserOutput(BaseModel):
        id: PydanticObjectId
        email: str
        nick_name: str

    owner: StudyUserOutput
    participants: List[StudyUserOutput]
    participants_wait: List[StudyUserOutput]
