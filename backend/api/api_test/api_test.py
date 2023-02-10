from fastapi import APIRouter

router = APIRouter()


@router.get("/get")
def get_test():
    return {"message": "test"}
