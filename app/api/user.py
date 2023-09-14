from fastapi import APIRouter, Depends

from app.core.security import verify_token

router = APIRouter()


@router.get("/me")
def read_user(tmp=Depends(verify_token)):
    # Cookie와 마찬가지로 header명과 같은 변수명을 입력해야 함
    # TODO
    # get access token in bearer header
    # check the token
    # if expired get refresh token return new access token
    # return user info
    print(tmp)
    return None


@router.put("/update")
def update_user():
    pass


@router.delete("/delete")
def delete_user():
    pass
