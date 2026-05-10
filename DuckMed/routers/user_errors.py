from fastapi import APIRouter, Query, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud import user_errors
from models.users import User
from config.db_conf import get_db
from schemas.user_errors import ErrorListResponse, ErrorItemResponse
from utils.auth import get_current_token
from utils.response import success_response
from schemas.user_errors import ChapterErrorDistributionResponse, ChapterErrorItem

router = APIRouter(prefix="/api/error", tags=["error"])

@router.get("/list")
async def get_error_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await user_errors.get_error_list(db, user.id, page, page_size)
    error_list = [ErrorItemResponse.model_validate({
        **question.__dict__,
        "error_id": error_id,
        "wrong_count": wrong_count,
        "created_at": created_at
    }) for question, wrong_count, created_at, error_id in rows]

    has_more = total > page * page_size
    data = ErrorListResponse(list=error_list, total=total, hasMore=has_more)
    return success_response(message="获取错题列表成功", data=data)

@router.delete("/delete/{question_id}")
async def delete_error(
    question_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    result = await user_errors.delete_error(db, user.id, question_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="错题不存在")
    return success_response(message="删除错题成功")

@router.delete("/clear")
async def clear_error(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    result = await user_errors.clear_error(db, user.id)
    return success_response(message="清空错题本成功")

@router.get("/statistics")
async def get_error_statistics(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    data = await user_errors.get_error_statistics(db, user.id)
    return success_response(message="查询成功", data=data)

# ==================== 错题章节分布折线图接口 ====================
@router.get("/chapter-distribution", response_model=ChapterErrorDistributionResponse)
async def get_chapter_error_distribution(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    # 拿到 字典列表
    data_list = await user_errors.get_error_chapter_distribution(db, user.id)

    # 路由里统一转 Schema
    items = [ChapterErrorItem(**item) for item in data_list]

    # 包装返回
    response = ChapterErrorDistributionResponse(list=items)
    return success_response(message="获取章节错题分布成功", data=response)