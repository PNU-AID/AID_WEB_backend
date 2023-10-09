from datetime import datetime

from app.models import Study, User


async def create_study_in_db(title, content, owner: User, max_participants: int, expire_time: datetime):
    """Create Study"""
    study = Study(title=title, content=content, owner=owner, max_participants=max_participants, expire_time=expire_time)

    await study.create()

    return study
