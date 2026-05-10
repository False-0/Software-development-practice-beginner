from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from models.questions import Questions
from models.user_favorites import UserFavorites


# 检查收藏状态：当前用户是否收藏了这道题目
async def is_question_favorite(
    db: AsyncSession,
    user_id: int,
    question_id: int
):
    query = select(UserFavorites).where(
        UserFavorites.user_id == user_id,
        UserFavorites.question_id == question_id
    )
    result = await db.execute(query)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None


# 添加题目收藏
async def add_question_favorite(
    db: AsyncSession,
    user_id: int,
    question_id: int
):
    favorite = UserFavorites(user_id=user_id, question_id=question_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


# 取消题目收藏
async def remove_question_favorite(
    db: AsyncSession,
    user_id: int,
    question_id: int
):
    stmt = delete(UserFavorites).where(
        UserFavorites.user_id == user_id,
        UserFavorites.question_id == question_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# 获取收藏列表（分页 + 联表查询）
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    # 总数
    count_query = select(func.count()).where(UserFavorites.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    # 联表查询：题目 + 收藏时间 + 收藏ID
    query = (
        select(
            Questions,
            UserFavorites.created_at.label("favorite_time"),
            UserFavorites.id.label("favorite_id")
        )
        .join(UserFavorites, UserFavorites.question_id == Questions.id)
        .where(UserFavorites.user_id == user_id)
        .order_by(UserFavorites.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query)
    rows = result.all()
    return rows, total


# 清空当前用户所有题目收藏
async def remove_all_favorites(
        db: AsyncSession,
        user_id: int
):
    stmt = delete(UserFavorites).where(UserFavorites.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0