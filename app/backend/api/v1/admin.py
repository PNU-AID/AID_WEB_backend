from fastapi import APIRouter

router = APIRouter()


@router.get("/read")
def read_all():
    pass


@router.get("/detail")
def read_one():
    pass


@router.post("/change_status")
async def change_pass_status():
    pass
