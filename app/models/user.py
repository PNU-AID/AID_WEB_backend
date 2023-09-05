from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserAuth(UserBase):
    password: str

    model_config = {"json_schema_extra": {"examples": [{"email": "test@test.com", "password": "qwer1234"}]}}


class SubmitForm(BaseModel):
    name: str
    student_id: str
    phone_number: str


class UserOut(UserBase):
    nick_name: Optional[str] = None
    is_member: bool = Field(default=False)
    is_admin: bool = Field(default=False)
    created_time: datetime = Field(default_factory=datetime.now)
    submission: Optional[SubmitForm] = None


class User(Document, UserOut):
    """User DB representation"""

    password: str

    @classmethod
    async def by_email(cls, email: EmailStr) -> "User":
        """Get User by Email"""
        return await cls.find_one(cls.email == email)

    class Settings:
        name = "users"
