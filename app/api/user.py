from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, Response

from app.core.security import get_access_token_header, get_token
from app.crud.user import delete_user, get_user_by_email, update_user
from app.schemas.auth import Token
from app.schemas.user import UserOut, UserUpdate

router = APIRouter(dependencies=[Depends(get_access_token_header)])


@router.get("/me", response_model=UserOut)
async def read_user_api(response: Response, token: Token = Depends(get_token)):
    user_email = token.email
    access_token = token.access_token
    user = await get_user_by_email(user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    response.headers["Authorization"] = f"Bearer {access_token}"

    return user


@router.put("/update", response_model=UserOut)
async def update_user_api(user_update: UserUpdate, response: Response, token: Token = Depends(get_token)):
    user_email = token.email
    access_token = token.access_token
    user = await update_user(user_update, user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    response.headers["Authorization"] = f"Bearer {access_token}"

    return user


@router.delete("/delete")
async def delete_user_api(response: Response, token: Token = Depends(get_token)):
    user_email = token.email
    user = await delete_user(user_email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # TODO
    # content 변경

    response = JSONResponse(content={"status": "success"})
    response.delete_cookie(key="refresh_token")
    return response
