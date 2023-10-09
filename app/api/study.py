from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.security import get_token
from app.crud.study import create_study_in_db, get_study_paginate
from app.crud.user import read_user_in_db
from app.schemas.auth import Token
from app.schemas.study import StudyBase

router = APIRouter()


@router.post("/create")
async def create_study(study_infos: StudyBase, token: Token = Depends(get_token)):
    user_email = token.email
    user = await read_user_in_db(user_email)
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    study_obj = await create_study_in_db(
        study_infos.title,
        study_infos.content,
        user,
        max_participants=study_infos.max_participants,
        expire_time=study_infos.expire_date,
    )
    print(str(study_obj))

    return JSONResponse(content={"status": "success"})


@router.get("/list")
async def get_study_list(page: int = 1, limit: int = 10):
    studies = get_study_paginate(page, limit)

    return studies
