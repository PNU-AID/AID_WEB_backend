from beanie.exceptions import DocumentNotFound
from pydantic import EmailStr

from app.models.user import User
from app.schemas.user import UserUpdate


async def get_user_by_email(email: EmailStr) -> User | None:
    """Get User by Email"""
    return await User.find_one(User.email == email)


async def update_user(new_user: UserUpdate, email: EmailStr) -> User | None:
    """Update User"""
    user = await User.find_one(User.email == email)
    if user is None:
        return None
    # TODO
    # for 문으로 수정 필요
    user.nick_name = new_user.nick_name
    user.submission = new_user.submission
    # try 쓸 필요 있나?
    try:
        await user.replace()
    except (ValueError, DocumentNotFound):
        print("Can't replace a non existing document")
    return user


async def delete_user(email: EmailStr) -> User | None:
    """Delete User"""
    user = await User.find_one(User.email == email)
    if user is None:
        return None
    await user.delete()
    return user
