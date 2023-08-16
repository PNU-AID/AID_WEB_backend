from backend.crud.submit import (
    create_submit,
    delete_submit,
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
    """지원자들이 지원하는 submit 제출하는 api<br/>
    Args:
    - (SubmitForm)

    Returns:<br/>
    - id: str 타입의 mongodb object id
    """
    inserted_id = create_submit(submission)
    return JSONResponse(content={"id": inserted_id}, status_code=status.HTTP_201_CREATED)


@router.get("/read", response_model=SubmitForm)
def get_my_submit(submit_id: str = Query()):
    """본인이 가진 id로 제출한 지원서 가져오는 api<br/>

    Args:
    - submit_id (str): mongodb id

    Returns:
    - (SubmitForm)
    """
    submit = read_submit(submit_id)
    return submit


@router.put("/modify")
def modify_my_submit(submit_id: str, submission: SubmitForm):
    """본인의 지원서 수정하는 api<br/>

    Args:
    - submit_id (str)
    - submission (SubmitForm)
    """
    update_submit(submit_id, submission)


@router.delete("/cancle")
def cancel_submit(submit_id: str):
    """지원서 삭제하는 api<br/>

    Args:
    - submit_id (str)
    """
    delete_submit(submit_id)
