from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.models.study import StudyStatus


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
