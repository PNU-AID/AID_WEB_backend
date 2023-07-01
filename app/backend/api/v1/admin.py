from fastapi import APIRouter

router = APIRouter()


@router.get("/read")
def read_all():
    pass


@router.get("/read")
def read_one(user_id: str):
    pass


@router.post("/change_status")
async def change_pass_status():
    pass
