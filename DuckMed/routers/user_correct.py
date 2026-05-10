from fastapi import APIRouter, Query, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_correct
from models.users import User
from config.db_conf import get_db
from schemas.user_correct import CorrectListResponse, CorrectItemResponse
from utils.auth import get_current_token
from utils.response import success_response

router = APIRouter(prefix="/api/correct", tags=["correct"])

@router.get("/list")
async def get_correct_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await user_correct.get_correct_list(db, user.id, page, page_size)
    correct_list = [CorrectItemResponse.model_validate({
        **question.__dict__,
        "correct_id": correct_id,
        "created_at": created_at
    }) for question, created_at, correct_id in rows]

    has_more = total > page * page_size
    data = CorrectListResponse(list=correct_list, total=total, hasMore=has_more)
    return success_response(message="获取做对题目成功", data=data)

@router.delete("/delete/{question_id}")
async def delete_correct(
    question_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    result = await user_correct.delete_correct(db, user.id, question_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    return success_response(message="删除成功")

@router.delete("/clear")
async def clear_correct(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    result = await user_correct.clear_correct(db, user.id)
    return success_response(message="清空成功")