from fastapi import APIRouter, Query, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from utils.auth import get_current_token
from utils.response import success_response
from models.users import User
from crud import user_favorites
from schemas.user_favorites import FavoriteCheckResponse,FavoriteAddRequest,FavoriteQuestionItemResponse,FavoriteListResponse

router = APIRouter(prefix="/api/favorite", tags=["favorite"])

# 1. 检查题目收藏状态
@router.get("/check", response_model=FavoriteCheckResponse)
async def check_question_favorite(
    question_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    is_fav = await user_favorites.is_question_favorite(db, user.id, question_id)
    return success_response(message="检查收藏状态成功",data=FavoriteCheckResponse(isFavorite =is_fav))


# 2. 添加收藏
@router.post("/add")
async def add_question_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    await user_favorites.add_question_favorite(db, user.id, data.question_id)
    return success_response(message="收藏成功")


# 3. 取消收藏
@router.delete("/cancel/{question_id}")
async def cancel_question_favorite(
    question_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    result = await user_favorites.remove_question_favorite(db, user.id, question_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="收藏不存在")
    return success_response(message="取消收藏成功")


# 4. 收藏列表 分页
@router.get("/list", response_model=FavoriteListResponse)
async def get_favorite_question_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await user_favorites.get_favorite_list(db, user.id, page, page_size)

    fav_list = [
        FavoriteQuestionItemResponse.model_validate({
            **question.__dict__,
            "favorite_id": fav_id,
            "favorite_time": fav_time
        })
        for question, fav_time, fav_id in rows
    ]

    has_more = total > page * page_size
    data = FavoriteListResponse(list=fav_list,total=total,hasMore=has_more)
    return success_response(message="获取收藏列表成功",data = data)


# 5. 清空全部收藏
@router.delete("/clear")
async def clear_all_favorite(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    await user_favorites.remove_all_favorites(db, user.id)
    return success_response(message="清空收藏成功")