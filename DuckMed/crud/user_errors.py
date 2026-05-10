from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date, timedelta
from sqlalchemy import select, delete, func,and_
from models.questions import  Questions,Chapters
from models.user_errors import UserError


# ==================== 1. 获取错题列表（分页 + 关联题目） ====================
async def get_error_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 10
):
    # 统计总数
    count_query = select(func.count(UserError.id)).where(UserError.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size

    # 查询列表（关联题目表）
    query = (
        select(
            Questions,
            UserError.wrong_count.label("wrong_count"),
            UserError.created_at.label("created_at"),
            UserError.id.label("error_id")
        )
        .join(UserError, UserError.question_id == Questions.id)
        .where(UserError.user_id == user_id)
        .order_by(UserError.updated_at.desc())
        .offset(offset)
        .limit(page_size)
    )

    result = await db.execute(query)
    rows = result.all()
    return rows, total


# ==================== 2. 删除单条错题 ====================
async def delete_error(
        db: AsyncSession,
        user_id: int,
        question_id: int
):
    stmt = delete(UserError).where(
        UserError.user_id == user_id,
        UserError.question_id == question_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# ==================== 3. 清空所有错题 ====================
async def clear_error(
        db: AsyncSession,
        user_id: int
):
    query = delete(UserError).where(UserError.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount or 0

# ==================== 4. 错题综合统计 ====================
async def get_error_statistics(db: AsyncSession, user_id: int):
    # 1. 总错题数【全部时间】
    total_stmt = select(func.count(UserError.id)).where(UserError.user_id == user_id)
    total_error = await db.scalar(total_stmt) or 0

    # 2. 今日时间区间：当天0点 ~ 现在
    today_zero = datetime.combine(date.today(), datetime.min.time())
    now_time = datetime.now()

    # 3. 今日错题数【仅今天】
    today_stmt = select(func.count(UserError.id)).where(
        UserError.user_id == user_id,
        and_(
            UserError.created_at >= today_zero,
            UserError.created_at <= now_time
        )
    )
    today_error = await db.scalar(today_stmt) or 0

    # 4. 今日错题最多章节
    chapter_stmt = (
        select(
            UserError.chapter_id,
            func.count(UserError.id).label("error_num")
        )
        .where(
            UserError.user_id == user_id,
            and_(
                UserError.created_at >= today_zero,
                UserError.created_at <= now_time
            )
        )
        .group_by(UserError.chapter_id)
        .order_by(func.count(UserError.id).desc())
        .limit(1)
    )
    res = await db.execute(chapter_stmt)
    top_chapter = res.first()

    if top_chapter:
        top_chapter_id = top_chapter.chapter_id
        top_chapter_num = top_chapter.error_num
    else:
        top_chapter_id = 0
        top_chapter_num = 0

    return {
        "total_error_count": total_error,
        "today_error_count": today_error,
        "top_chapter_id": top_chapter_id,
        "top_chapter_num": top_chapter_num
    }

# ==================== 章节错题分布（折线图专用） ====================
async def get_error_chapter_distribution(db: AsyncSession, user_id: int):
    query = (
        select(
            Chapters.name.label("chapter_name"),
            func.count(UserError.id).label("count")
        )
        .join(Chapters, UserError.chapter_id == Chapters.id)
        .where(UserError.user_id == user_id)
        .group_by(Chapters.id, Chapters.name)
        .order_by(Chapters.id)
    )
    result = await db.execute(query)
    rows = result.all()

    return [
        {
            "chapter_name": row.chapter_name,
            "count": row.count
        }
        for row in rows
    ]