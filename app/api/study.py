from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.security import get_token
from app.crud.study import (
    add_comment_to_study,
    add_liker_to_study,
    add_user_to_waitlist,
    create_study_in_db,
    delete_study_from_db,
    get_likers_from_study,
    get_owner_from_study,
    get_participants_wait_from_study,
    get_study_by_id,
    get_study_paginate,
    is_participants_left,
    move_waiter_to_participants,
    remove_user_from_study,
    update_study_in_db,
)
from app.crud.user import read_user_in_db
from app.models.study import Study, StudyStatus
from app.schemas.auth import Token
from app.schemas.study import (
    StudyComment,
    StudyCreate,
    StudyOutput,
    StudyOutputSimple,
    StudyUpdate,
)

router = APIRouter()


@router.post("/create")
async def create_study(study_infos: StudyCreate, token: Token = Depends(get_token)) -> Study:
    """스터디 생성

    로그인 한 사람만 생성 가능
    """
    user_email = token.email
    user = await read_user_in_db(user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    study = await create_study_in_db(study_infos, user)

    return study


# TODO : status별 조회 기능
# TODO : created_time순 정렬
@router.get("/list", response_model=List[StudyOutputSimple])
async def get_study_list(page: int = 1, limit: int = 10):
    """스터디 목록 조회

    page로 스터디 목록 페이지 설정
    limit로 페이지 별 스터디 개수 설정"""
    studies = await get_study_paginate(page, limit)
    return studies


@router.get("/list/{study_id}", response_model=StudyOutput)
async def get_study_info(study_id: str) -> Study:
    """스터디 ID로 정보 조회"""
    study = await get_study_by_id(study_id)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")

    await study.fetch_all_links()
    return study


@router.delete("/delete/{study_id}")
async def delete_study(study_id: str, token: Token = Depends(get_token)):
    """스터디 삭제

    스터디를 DB에서 완전히 제거
    owner만 삭제 가능"""
    user_email = token.email
    user = await read_user_in_db(user_email)
    study = await get_study_by_id(study_id)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    study_owner = await get_owner_from_study(study)
    if user_email != study_owner.email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not owner of this study")

    await delete_study_from_db(study)
    return JSONResponse(content={"status": "success"})


@router.patch("/update/{study_id}", response_model=StudyOutput)
async def update_study(study_id: str, study_update: StudyUpdate, token: Token = Depends(get_token)):
    """스터디 정보 업데이트"""
    study = await get_study_by_id(study_id)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")

    user_email = token.email
    user = await read_user_in_db(user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    study_owner = await get_owner_from_study(study)
    if user_email != study_owner.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not owner of this study")

    study_updated = await update_study_in_db(study_update, study)
    if isinstance(study_updated, str):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Study update failure: {study_updated}")

    study_updated.fetch_all_links()
    return study_updated


@router.patch("/join/{study_id}")
async def join_study(study_id: str, token: Token = Depends(get_token)):
    """스터디 참여 신청"""
    user_email = token.email
    user = await read_user_in_db(user_email)
    study = await get_study_by_id(study_id)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if study.status != StudyStatus.open:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Study is not open")

    await study.fetch_all_links()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    if user in study.participants:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already joined this study")
    if user in study.participants_wait:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already waiting to join this study")

    await add_user_to_waitlist(study, user)
    return JSONResponse(content={"status": "success"})


@router.patch("/approve/{study_id}")
async def approve_waiting_user(study_id: str, user_email: str, token: Token = Depends(get_token)):
    """스터디 참여 신청 승인

    owner만 가능"""
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(user_email)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    study_owner = await get_owner_from_study(study)
    participants_wait = await get_participants_wait_from_study(study)
    if not await is_participants_left(study):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No more participants can join this study")
    if token.email != study_owner.email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not owner of this study")
    if target_user not in participants_wait:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not waiting to join this study")

    await move_waiter_to_participants(study, target_user)
    return JSONResponse(content={"status": "success"})


@router.patch("/like/{study_id}")
async def add_like(study_id: str, token: Token = Depends(get_token)):
    """스터디 좋아요"""
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(token.email)
    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    liker_IDs = await get_likers_from_study(study)
    if target_user in liker_IDs:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Already liked this post")

    await add_liker_to_study(study, target_user)

    return JSONResponse(content={"status": "success"})


@router.get("/like/{study_id}")
async def get_like(study_id: str, token: Token = Depends(get_token)):
    """스터디 좋아요 개수, 사용자가 좋아요 눌렀는지 여부 조회"""
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(token.email)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    liker_IDs = await get_likers_from_study(study)

    return JSONResponse(content={"like_count": study.likes.likeCount, "is_liked": target_user in liker_IDs})


@router.patch("/comment/{study_id}")
async def add_comment(study_id: str, comment_input: StudyComment, token: Token = Depends(get_token)):
    """댓글 추가"""
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(token.email)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    await add_comment_to_study(study, target_user, comment_input.comment)

    return JSONResponse(content={"status": "success"})


@router.patch("/quit/{study_id}", response_model=StudyOutput)
async def quit_study(study_id: str, token: Token = Depends(get_token)):
    """스터디 나가기"""
    study = await get_study_by_id(study_id)
    target_user = await read_user_in_db(token.email)

    if study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find study with given id")
    if target_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    await study.fetch_link(Study.participants)
    if target_user not in study.participants:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not in this study")

    study = await remove_user_from_study(study, target_user)
    return study
