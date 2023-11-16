import random
from datetime import datetime

from app.models import Study, User
from app.models.study import CommentForm
from app.schemas.study import StudyCreate, StudyUpdate


async def create_study_in_db(study_infos: StudyCreate, owner: User):
    """Create Study"""
    title = study_infos.title
    content = study_infos.content
    max_participants = study_infos.max_participants
    expire_time = study_infos.expire_time
    url = study_infos.url if study_infos.url else None

    study = Study(
        title=title, content=content, owner=owner, max_participants=max_participants, expire_time=expire_time, url=url
    )

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


async def delete_study_from_db(study: Study):
    await study.delete()


async def get_participants_wait_from_study(study: Study):
    await study.fetch_link(Study.participants_wait)

    return study.participants_wait


async def get_likers_from_study(study: Study):
    await study.fetch_link(Study.likes.likeID)

    return study.likes.likeID


async def add_liker_to_study(study: Study, user: User):
    study.likes.likeID.append(user)
    study.likes.likeCount = len(study.likes.likeID)
    await study.replace()


async def is_participants_left(study: Study) -> bool:
    return study.cur_participants < study.max_participants


async def move_waiter_to_participants(study: Study, user: User):
    # TODO : remove -> pull?
    study.participants_wait.remove(user)
    study.participants.append(user)
    study.cur_participants = len(study.participants)
    await study.replace()


async def add_comment_to_study(study: Study, writer: User, comment: str):
    comment_obj = CommentForm(writer=writer, content=comment)
    study.comments.append(comment_obj)
    await study.replace()


async def update_study_in_db(study_update: StudyUpdate, study: Study) -> Study | str:
    await study.fetch_all_links()
    target_user = await User.get(study_update.owner_id)

    study.title = study_update.title
    study.content = study_update.content
    study.max_participants = study_update.max_participants
    study.expire_time = study_update.expire_time
    study.owner = target_user
    study.status = study_update.status
    study.url = study_update.url

    # print(study_update.expire_time.tzinfo, datetime.now().tzinfo)
    tz = study_update.expire_time.tzinfo

    if target_user is None:
        return "Can't find user with given id."
    if study_update.max_participants < study.cur_participants:
        return "Can't update max_participants to lower than current participants."
    if study_update.expire_time < datetime.now(tz):
        return "Can't update expire_time to lower than current time."
    if study.expire_time < datetime.now(tz) and study_update.status == "open":  # Not tested
        return "Can't open expired study."
    if target_user not in study.participants:
        return "Can't update owner to non-participant."

    await study.replace()
    return study


async def add_user_to_waitlist(study: Study, user: User):
    study.participants_wait.append(user)
    await study.replace()


async def remove_user_from_study(study: Study, user: User):
    await study.fetch_link(Study.owner)
    study.participants.remove(user)
    if study.owner == user:
        study.owner = random.choice(study.participants)
    study.cur_participants = len(study.participants)

    await study.replace()

    return study
