from pydantic import EmailStr

from app.models.user import User


async def get_user_by_email(email: EmailStr) -> User:
    """Get User by Email"""
    return await User.find_one(User.email == email)
