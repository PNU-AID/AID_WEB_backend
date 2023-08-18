from backend.core.utils import make_message
from backend.crud.submit import (
    create_submit,
    delete_submit,
    read_submit,
    update_submit,
)
from backend.scheme.submit import SubmitForm
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

# submit에 관한 api를 담은 코드

router = APIRouter()  # submit ROUTER 를 선언해준다.


@router.post("/create")
def upload_submit(submission: SubmitForm):
    """지원자들이 지원하는 submit 제출하는 api<br/>
    Args:
    - (SubmitForm)

    Returns:<br/>
    - id (str): str 타입의 mongodb object id
    """
    inserted_id = create_submit(submission.model_dump())
    return JSONResponse(content={"id": inserted_id}, status_code=status.HTTP_201_CREATED)


@router.get("/read", response_model=SubmitForm)
def get_my_submit(submit_id: str):
    """본인이 가진 id로 제출한 지원서 가져오는 api<br/>

    Args:
    - submit_id (str): mongodb id

    Returns:
    - (SubmitForm)
    """

    try:
        submit = read_submit(submit_id)
    except Exception:
        # ObjectId must be a 12-byte input or a 24-character hex string
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")

    if submit is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")

    return submit


@router.put("/modify")
def modify_my_submit(submit_id: str, submission: SubmitForm):
    """본인의 지원서 수정하는 api<br/>

    Args:
    - submit_id (str)
    - submission (SubmitForm)
    """
    try:
        update_submit(submit_id, submission.model_dump())
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")
    return make_message("modify success")


@router.delete("/cancle")
def cancel_submit(submit_id: str):
    """지원서 삭제하는 api<br/>

    Args:
    - submit_id (str)
    """
    try:
        delete_submit(submit_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID is not found")
    return make_message("delete success")
