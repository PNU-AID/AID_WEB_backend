from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.security import get_token
from app.crud.study import (
    create_study_in_db,
    get_owner_from_study,
    get_participants_wait_from_study,
    get_study_by_id,
    get_study_paginate,
    is_participants_left,
    move_waiter_to_participants,
)
from app.crud.user import read_user_in_db
from app.schemas.auth import Token
from app.schemas.study import StudyBase, StudyUpdate

router = APIRouter()


@router.post("/create")
async def create_study(study_infos: StudyBase, token: Token = Depends(get_token)):
    user_email = token.email
    user = await read_user_in_db(user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    await create_study_in_db(
        study_infos.title,
        study_infos.content,
        user,
        max_participants=study_infos.max_participants,
        expire_time=study_infos.expire_date,
    )

    return JSONResponse(content={"status": "success"})


@router.get("/list")
async def get_study_list(page: int = 1, limit: int = 10):
    studies = await get_study_paginate(page, limit)

    return studies


@router.delete("/delete/{study_id}")
async def delete_study(study_id: str, token: Token = Depends(get_token)):
    study = await get_study_by_id(study_id)
    study_owner = await get_owner_from_study(study)

    user_email = token.email
    user = await read_user_in_db(user_email)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    if user_email != study_owner.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not owner of this study")

    await study.delete()
    return JSONResponse(content={"status": "success"})


@router.patch("/update/{study_id}")
async def update_study(study_id: str, study_update: StudyUpdate, token: Token = Depends(get_token)):
    # TODO
    # 세부 구현 사항 논의 필요
    study = await get_study_by_id(study_id)
    # study_owner = await get_owner_from_study(study)

    user_email = token.email
    await read_user_in_db(user_email)

    await get_owner_from_study(study)


@router.patch("/join/{study_id}")
async def join_study(study_id: str, token: Token = Depends(get_token)):
    study = await get_study_by_id(study_id)
    user_email = token.email
    user = await read_user_in_db(user_email)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    await study.fetch_all_links()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    if user in study.participants:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already joined this study")
    if user in study.participants_wait:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already waiting to join this study")

    study.participants_wait.append(user)
    await study.replace()
    return JSONResponse(content={"status": "success"})


@router.patch("/approve/{study_id}")
async def approve_waiting_user(study_id: str, user_email: str, token: Token = Depends(get_token)):
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(user_email)
    print(target_user.id)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    study_owner = await get_owner_from_study(study)
    participants_wait = await get_participants_wait_from_study(study)
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    if not await is_participants_left(study):
        raise HTTPException(status_code=400, detail="No more participants can join this study")
    if token.email != study_owner.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not owner of this study")
    if target_user not in participants_wait:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not waiting to join this study")

    await move_waiter_to_participants(study, target_user)
    return JSONResponse(content={"status": "success"})
