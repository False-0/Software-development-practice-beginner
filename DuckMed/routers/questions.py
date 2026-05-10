from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud import questions
from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_token

# 创建路由：前缀 /api/question，分组标签 question
router = APIRouter(prefix="/api/question", tags=["question"])

# ===================== 1. 获取所有科目 =====================
@router.get("/subjects")
async def get_subjects(
    skip: int = Query(0, ge=0, description="跳过条数"),
    limit: int = Query(100, ge=1, le=1000, description="每页条数"),
    db: AsyncSession = Depends(get_db)
):
    subjects = await questions.get_subjects(db, skip, limit)
    return {
        "code": 200,
        "message": "获取科目列表成功",
        "data": subjects
    }

# ===================== 2. 根据科目ID获取章节列表 =====================
@router.get("/chapters")
async def get_chapters(
    subject_id: int = Query(..., alias="subjectId", description="科目ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, alias="pageSize", ge=1, le=100, description="每页条数"),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    chapters = await questions.get_chapters_by_subject(db, subject_id, offset, page_size)
    total = await questions.get_chapter_count(db, subject_id)
    has_more = (offset + len(chapters)) < total

    return {
        "code": 200,
        "message": "获取章节列表成功",
        "data": {
            "list": chapters,
            "total": total,
            "hasMore": has_more
        }
    }

# ===================== 3. 根据章节ID获取题目列表 =====================
@router.get("/list")
async def get_questions_list(
    chapter_id: int = Query(..., alias="chapterId", description="章节ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, alias="pageSize", ge=1, le=100, description="每页条数"),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * page_size
    question_list = await questions.get_questions_by_chapter(db, chapter_id, offset, page_size)
    total = await questions.get_question_count(db, chapter_id)
    has_more = (offset + len(question_list)) < total

    return {
        "code": 200,
        "message": "获取题目列表成功",
        "data": {
            "list": question_list,
            "total": total,
            "hasMore": has_more
        }
    }

# ===================== 4. 获取单个题目详情 =====================
@router.get("/detail")
async def get_question_detail(
    question_id: int = Query(..., alias="id", description="题目ID"),
    db: AsyncSession = Depends(get_db)
):
    # 获取题目详情
    question_detail = await questions.get_question_detail(db, question_id)
    if not question_detail:
        raise HTTPException(status_code=404, detail="题目不存在")

    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": question_detail.id,
            "title": question_detail.title,
            "optionA": question_detail.option_a,
            "optionB": question_detail.option_b,
            "optionC": question_detail.option_c,
            "optionD": question_detail.option_d,
            "answer": question_detail.answer,
            "chapterId": question_detail.chapter_id,
            "createdAt": question_detail.created_at.strftime("%Y-%m-%dT%H:%M:%S")  # 统一时间格式
        }
    }

# ==================== 【核心】用户提交答案 ====================
@router.post("/submit")
async def submit_answer(
    question_id: int = Query(..., description="题目ID"),
    answer: str = Query(..., regex=r'^[A-Da-d]$', description="用户答案（A/B/C/D）"),
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    res = await questions.submit_answer(db, user.id, question_id, answer)
    # 统一响应格式，兼容内部返回的error状态
    if res.get("status") == "error":
        raise HTTPException(status_code=400, detail=res["msg"])
    return {
        "code": 200,
        "message": "提交答案成功",
        "data": res
    }