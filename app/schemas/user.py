from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.user import SubmitForm


class UserBase(BaseModel):
    email: EmailStr


class UserAuth(UserBase):
    password: str

    model_config = {"json_schema_extra": {"examples": [{"email": "test@test.com", "password": "qwer1234"}]}}


class UserOut(UserBase):
    nick_name: str
    is_member: bool
    is_admin: bool
    created_time: datetime
    submission: Optional[SubmitForm]
