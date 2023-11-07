from datetime import datetime

from app.models import Study, User
from app.models.study import CommentForm
from app.schemas.study import StudyUpdate


async def create_study_in_db(title, content, owner: User, max_participants: int, expire_time: datetime):
    """Create Study"""
    study = Study(title=title, content=content, owner=owner, max_participants=max_participants, expire_time=expire_time)

    await study.create()

    return study


async def get_study_paginate(page: int, limit: int):
    start_idx = (page - 1) * limit
    content = await Study.find().limit(limit).skip(start_idx).to_list()

    return content


async def get_study_by_id(study_id: str):
    content = await Study.get(study_id)

    return content


async def get_owner_from_study(study: Study):
    await study.fetch_link(Study.owner)

    return study.owner


async def get_participants_wait_from_study(study: Study):
    await study.fetch_link(Study.participants_wait)

    return study.participants_wait


async def get_likers_from_study(study: Study):
    await study.fetch_link(Study.likes.likeID)

    return study.likes.likeID


async def is_participants_left(study: Study):
    return study.cur_participants < study.max_participants


async def move_waiter_to_participants(study: Study, user: User):
    study.participants_wait.remove(user)
    study.participants.append(user)
    study.cur_participants = len(study.participants)
    await study.replace()


async def add_comment_to_study(study: Study, writer: User, comment: str):
    comment_obj = CommentForm(writer=writer, content=comment)
    study.comments.append(comment_obj)
    await study.replace()


async def update_study_in_db(study_update: StudyUpdate, study: Study):
    target_user = await User.get(study_update.owner_id)
    if target_user is None:
        return None

    study.title = study_update.title
    study.content = study_update.content
    study.max_participants = study_update.max_participants
    study.expire_time = study_update.expire_time
    study.owner = target_user
    study.status = study_update.status

    await study.replace()
    return study
