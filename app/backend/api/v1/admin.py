from backend.core.security import get_admin
from backend.crud.submit import (
    change_status,
    read_all_submit,
    read_submit,
)
from backend.scheme.submit import SubmitForm
from fastapi import APIRouter, Body, Depends, HTTPException, status

router = APIRouter()


@router.get("/read_all")
def read_all(admin: str = Depends(get_admin)):
    submit_list = read_all_submit()
    return submit_list


@router.get("/read_one", response_model=SubmitForm)
def read_one(submit_id: str, admin: str = Depends(get_admin)):
    try:
        submit = read_submit(submit_id)
    except Exception:
        # ObjectId must be a 12-byte input or a 24-character hex string
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")

    if submit is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")
    print(submit)
    return submit


@router.post("/change_status")
async def change_pass_status(submit_id: str = Body(), status: bool = Body(), admin: str = Depends(get_admin)):
    change_status(submit_id, status)
