from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel

from ..models.study import statusEnum


class StudyBase(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_date: datetime

    model_config = {"json_schema_extra": {"examples": [{"title": "test_title", "content": "test_content"}]}}


class StudyUpdate(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_date: datetime
    owner_id: PydanticObjectId
    status: statusEnum
