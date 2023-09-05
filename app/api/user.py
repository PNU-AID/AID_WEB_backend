from fastapi import APIRouter

router = APIRouter()


@router.get("/user/me")
def read_user():
    pass


@router.put("/user/update")
def update_user():
    pass


@router.delete("/user/delete")
def delete_user():
    pass
