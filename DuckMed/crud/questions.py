from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.questions import Subjects, Chapters, Questions
from models.user_correct import UserCorrect
from models.user_errors import UserError
from models.user_statistics import UserStatistics


# ===================== 科目 Subjects 操作 =====================
async def get_subjects(db: AsyncSession, skip: int = 0, limit: int = 100):
    """获取所有科目列表"""
    stmt = select(Subjects).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_subject_detail(db: AsyncSession, subject_id: int):
    """获取单个科目详情"""
    stmt = select(Subjects).where(Subjects.id == subject_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ===================== 章节 Chapters 操作 =====================
async def get_chapters_by_subject(
        db: AsyncSession,
        subject_id: int,
        skip: int = 0,
        limit: int = 100
):
    """根据科目ID获取该科目下的所有章节"""
    stmt = select(Chapters).where(Chapters.subject_id == subject_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_chapter_count(db: AsyncSession, subject_id: int):
    """查询指定科目下的章节数量"""
    stmt = select(func.count(Chapters.id)).where(Chapters.subject_id == subject_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_chapter_detail(db: AsyncSession, chapter_id: int):
    """获取单个章节详情"""
    stmt = select(Chapters).where(Chapters.id == chapter_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ===================== 试题 Questions 操作 =====================
async def get_questions_by_chapter(
        db: AsyncSession,
        chapter_id: int,
        skip: int = 0,
        limit: int = 10
):
    """根据章节ID获取该章节下的所有试题（分页）"""
    stmt = select(Questions).where(Questions.chapter_id == chapter_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_question_count(db: AsyncSession, chapter_id: int):
    """查询指定章节下的题目数量"""
    stmt = select(func.count(Questions.id)).where(Questions.chapter_id == chapter_id)
    result = await db.execute(stmt)
    return result.scalar_one()


async def get_question_detail(db: AsyncSession, question_id: int):
    """获取单个试题详情（含选项、答案）"""
    stmt = select(Questions).where(Questions.id == question_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# ==================== 用户提交答案 ====================
async def submit_answer(
    db: AsyncSession,
    user_id: int,
    question_id: int,
    user_answer: str
):
    # 1. 获取题目正确答案
    question = await get_question_detail(db, question_id)
    if not question:
        return {"status": "error", "msg": "题目不存在"}

    correct_answer = question.answer
    is_correct = user_answer.upper() == correct_answer.upper()

    chapter = await get_chapter_detail(db, question.chapter_id)
    subject_id = chapter.subject_id if chapter else None
    chapter_id = question.chapter_id


    if is_correct:
        correct = UserCorrect(
            user_id=user_id,
            question_id=question_id,
            subject_id=subject_id,
            chapter_id=chapter_id
        )
        db.add(correct)
        await db.commit()
        await db.refresh(correct)
    else:
        stmt = select(UserError).where(
            UserError.user_id == user_id,
            UserError.question_id == question_id
        )
        result = await db.execute(stmt)
        error_item = result.scalar_one_or_none()

        if error_item:
            # 已存在 → 次数+1
            error_item.wrong_count += 1
            await db.commit()
            await db.refresh(error_item)
        else:
            # 不存在 → 新增
            error_item = UserError(
                user_id=user_id,
                question_id=question_id,
                subject_id=subject_id,
                chapter_id=chapter_id,
                wrong_count=1
            )
            db.add(error_item)
            await db.commit()
            await db.refresh(error_item)

    # 处理用户统计
    stat_query = select(UserStatistics).where(UserStatistics.user_id == user_id)
    stat_result = await db.execute(stat_query)
    user_stat = stat_result.scalar_one_or_none()

    if not user_stat:
        # 没有就创建
        user_stat = UserStatistics(user_id=user_id)
        db.add(user_stat)
        await db.commit()

    # 总做题数 +1
    user_stat.total_done += 1
    # 做对了，正确数 +1
    if is_correct:
        user_stat.total_correct += 1

    await db.commit()
    await db.refresh(user_stat)  # 统计对象刷新

    return {
        "status": "success",
        "is_correct": is_correct,
        "correct_answer": correct_answer
    }