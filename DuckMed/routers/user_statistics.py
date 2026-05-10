from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from utils.auth import get_current_token
from models.users import User
from crud import user_statistics
from utils.response import success_response
from schemas.user_statistics import RankInfoResponse, Top3Item

router = APIRouter(prefix="/api/rank", tags=["刷题排行榜"])

@router.get("/info")
async def get_rank_info(
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    # 1. 排名
    my_rank = await user_statistics.get_user_rank(db, user.id)

    # 2. 个人统计
    total_done, total_correct, correct_rate = await user_statistics.get_user_stat_info(db, user.id)

    # 3. 前三名
    top3_rows = await user_statistics.get_top3_ranking(db)
    top3 = [
        Top3Item(**{"username": row.username, "totalDone": row.total_done})
        for row in top3_rows
    ]

    # 4. 统一返回格式
    data = {
        "myRank": my_rank,
        "totalDone": total_done,
        "totalCorrect": total_correct,
        "correctRate": correct_rate,
        "top3": top3
    }

    return success_response(data=data)