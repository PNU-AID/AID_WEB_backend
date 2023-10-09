from datetime import datetime

from pydantic import BaseModel


class StudyBase(BaseModel):
    title: str
    content: str
    max_participants: int
    expire_date: datetime

    model_config = {"json_schema_extra": {"examples": [{"title": "test_title", "content": "test_content"}]}}
