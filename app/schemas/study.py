from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from app.models.study import statusEnum


class StudyBase(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_time: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "test_title",
                    "content": "test_content",
                    "max_participants": 10,
                    "expire_time": str(datetime.now()),
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
    status: statusEnum


class StudyComment(BaseModel):
    comment: str
