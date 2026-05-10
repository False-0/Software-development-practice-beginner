from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from models.user_statistics import UserStatistics
from models.users import User


# 获取用户刷题排名
async def get_user_rank(db: AsyncSession, user_id: int):
    rank_subquery = select(
        UserStatistics.user_id,
        func.rank().over(order_by=desc(UserStatistics.total_done)).label("rank_num")
    ).subquery()

    query = select(rank_subquery.c.rank_num).where(rank_subquery.c.user_id == user_id)
    res = await db.execute(query)
    return res.scalar() or 9999


# 获取用户统计信息
async def get_user_stat_info(db: AsyncSession, user_id: int):
    query = select(UserStatistics).where(UserStatistics.user_id == user_id)
    res = await db.execute(query)
    stat = res.scalar_one_or_none()

    if not stat:
        return 0, 0, 0.0

    total_done = stat.total_done
    total_correct = stat.total_correct

    if total_done <= 0:
        correct_rate = 0.0
    else:
        correct_rate = round((total_correct / total_done) * 100, 2)

    return total_done, total_correct, correct_rate


# 获取前三名（图表数据）
async def get_top3_ranking(db: AsyncSession):
    query = (
        select(User.username, UserStatistics.total_done)
        .join(User, User.id == UserStatistics.user_id)
        .order_by(desc(UserStatistics.total_done))
        .limit(3)
    )
    res = await db.execute(query)
    return res.all()