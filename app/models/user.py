from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, Field

from app.core.utils import get_random_name


class SubmitForm(BaseModel):
    name: str
    student_id: str
    phone_number: str


class User(Document):
    """User DB representation"""

    email: EmailStr
    nick_name: Optional[str] = Field(default_factory=get_random_name)
    is_member: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    created_time: datetime = Field(default_factory=datetime.now)
    submission: Optional[SubmitForm] = None
    password: str

    class Settings:
        name = "user"
