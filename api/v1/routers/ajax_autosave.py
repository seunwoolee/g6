from typing_extensions import Annotated, List

from fastapi import  APIRouter, Path, Depends

from core.models import Member
from api.v1.dependencies.member import get_current_member
from api.v1.models.ajax import (
     AutoSaveModel, ResponseAutoSaveModel, 
     ResponseAutoSaveCountModel, ResponseAutoSaveDeleteModel,
)
from service.ajax import AJAXService


router = APIRouter()


@router.get("/autosave_list",
            summary="자동저장 목록",
            responses={**AJAXService.responses}
            )
async def autosave_list(
    member: Annotated[Member, Depends(get_current_member)],
    ajax_service: Annotated[AJAXService, Depends()],
) -> List[ResponseAutoSaveModel]:
    """자동저장 목록을 반환한다."""
    ajax_service.validate_login(member)
    save_list = ajax_service.get_autosave_list(member)
    return save_list


@router.get("/autosave_count",
            summary="자동저장글 개수",
            responses={**AJAXService.responses}
            )
async def autosave_count(
    member: Annotated[Member, Depends(get_current_member)],
    ajax_service: Annotated[AJAXService, Depends()]
) -> ResponseAutoSaveCountModel:
    """자동저장글 개수를 반환한다."""
    ajax_service.validate_login(member)
    return {"count": ajax_service.get_autosave_count(member.mb_id)}


@router.get("/autosave_load/{as_id}",
            summary="자동저장글 불러오기",
            responses={**AJAXService.responses}
            )
async def autosave_load(
    member: Annotated[Member, Depends(get_current_member)],
    ajax_service: Annotated[AJAXService, Depends()],
    as_id: int = Path(..., title="자동저장 ID", description="자동저장 ID")
) -> ResponseAutoSaveModel:
    """자동저장 내용을 불러온다."""
    ajax_service.validate_login(member)
    save_data = ajax_service.get_autosave_content(as_id, member)
    return save_data


@router.post("/autosave",
             summary="자동저장",
             responses={**AJAXService.responses}
             )
async def autosave(
    member: Annotated[Member, Depends(get_current_member)],
    ajax_service: Annotated[AJAXService, Depends()],
    data: AutoSaveModel
) -> ResponseAutoSaveCountModel:
    """
    작성중인 게시글을 임시 저장한다.
    return: 자동저장글 개수

    ### Request Body
    - **as_uid**: 자동저장 UID
    - **as_subject**: 자동저장 글 제목
    - **as_content**: 자동저장 글 내용
    """
    ajax_service.validate_login(member)
    ajax_service.autosave_save(member, data)
    count = ajax_service.get_autosave_count(member.mb_id)
    return {"count": count}


@router.delete("/autosave/{as_id}",
                summary="자동저장글 삭제",
                responses={**AJAXService.responses}
               )
async def autosave_delete(
    member: Annotated[Member, Depends(get_current_member)],
    ajax_service: Annotated[AJAXService, Depends()],
    as_id: int = Path(..., title="자동저장 ID", description="자동저장 ID")
) -> ResponseAutoSaveDeleteModel:
    """임시저장글을 삭제한다."""
    ajax_service.validate_login(member)
    ajax_service.autosave_delete(as_id, member)
    return {"result": "deleted"}