from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    email: EmailStr
    access_token: str
