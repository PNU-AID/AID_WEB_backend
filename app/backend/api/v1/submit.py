from backend.crud.submit import (
    create_submit,
    read_submit,
    update_submit,
)
from backend.scheme.submit import SubmitForm
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

# submit에 관한 api를 담은 코드

router = APIRouter()  # submit ROUTER 를 선언해준다.


@router.post("/create")
def upload_submit(submission: SubmitForm):
    inserted_id = create_submit(submission)
    return JSONResponse(content={"id": inserted_id}, status_code=status.HTTP_201_CREATED)


@router.get("/read")
def get_my_submit(submit_id: str = Query()):
    submit = read_submit(submit_id)
    del submit["_id"]
    return submit


@router.put("/modify")
def modify_my_submit(submit_id: str, submission: SubmitForm):
    update_submit(submit_id, submission)


@router.delete("/cancle")
def cancel_submit():
    pass
