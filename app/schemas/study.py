from pydantic import BaseModel


class StudyBase(BaseModel):
    title: str
    content: str

    model_config = {"json_schema_extra": {"examples": [{"title": "test_title", "content": "test_content"}]}}
