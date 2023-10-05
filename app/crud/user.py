from pydantic import EmailStr

from app.models.user import User
from app.schemas.user import UserUpdate


async def read_user_in_db(email: EmailStr) -> User:
    """Get User by Email"""
    return await User.find_one(User.email == email)


async def create_user_in_db(email: EmailStr, password: str):
    user = User(email=email, password=password)
    await user.create()
    return user


async def update_user_in_db(user_update: UserUpdate):
    user = await User.find_one(User.email == user_update.email)
    user.nick_name = user_update.nick_name
