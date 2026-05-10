from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from models.questions import  Questions
from models.user_correct import UserCorrect


# ==================== 1. 获取做对题目列表（分页 + 关联题目） ====================
async def get_correct_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    # 统计总数
    count_query = select(func.count(UserCorrect.id)).where(UserCorrect.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    # 查询列表（关联题目表）
    query = (
        select(
            Questions,
            UserCorrect.created_at.label("created_at"),
            UserCorrect.id.label("correct_id")
        )
        .join(UserCorrect, UserCorrect.question_id == Questions.id)
        .where(UserCorrect.user_id == user_id)
        .order_by(UserCorrect.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query)
    rows = result.all()
    return rows, total


# ==================== 2. 删除单条做对记录 ====================
async def delete_correct(
        db: AsyncSession,
        user_id: int,
        question_id: int
):
    stmt = delete(UserCorrect).where(
        UserCorrect.user_id == user_id,
        UserCorrect.question_id == question_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# ==================== 3. 清空所有做对记录 ====================
async def clear_correct(
        db: AsyncSession,
        user_id: int
):
    query = delete(UserCorrect).where(UserCorrect.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0