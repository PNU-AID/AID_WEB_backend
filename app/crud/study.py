from datetime import datetime

from app.models import Study, User


async def create_study_in_db(title, content, owner: User, max_participants: int, expire_time: datetime):
    """Create Study"""
    study = Study(title=title, content=content, owner=owner, max_participants=max_participants, expire_time=expire_time)

    await study.create()

    return study


async def get_study_paginate(page: int, limit: int):
    start_idx = (page - 1) * limit
    content = await Study.find().limit(limit).skip(start_idx).to_list()

    return content
