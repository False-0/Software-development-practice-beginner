from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from utils.auth import get_current_token
from models.users import User
from crud import forum
from schemas.forum import *
from utils.response import success_response

router = APIRouter(prefix="/api/forum", tags=["论坛"])

# ==================== 帖子列表 ====================
@router.get("/list")
async def get_post_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    db: AsyncSession = Depends(get_db)
):
    rows, total = await forum.get_post_list(db, page, page_size)
    post_list = [
        PostItemResponse.model_validate({
            **post.__dict__,
            "post_id": post.id,
            "title": post.title,
            "view_count": post.view_count,
            "created_at": post.created_at
        }) for post in rows
    ]

    has_more = total > page * page_size
    data = PostListResponse(list=post_list, total=total, hasMore=has_more)
    return success_response(message="获取帖子列表成功", data=data)

# ==================== 热门帖子 TOP10 ====================
@router.get("/hot")
async def get_hot_posts(
    db: AsyncSession = Depends(get_db)
):
    rows = await forum.get_hot_posts(db)
    hot_list = [
        HotPostItemResponse.model_validate({
            **post.__dict__,
            "post_id": post.id,
            "title": post.title,
            "view_count": post.view_count
        }) for post in rows
    ]
    return success_response(data={"list": hot_list})

# ==================== 发布帖子 ====================
@router.post("/create")
async def create_post(
    req: CreatePostRequest,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    await forum.create_post(db, user.id, req.title, req.content)
    return success_response(message="发布帖子成功")


# ==================== 帖子详情 + 评论 ====================
@router.get("/detail/{post_id}")
async def get_post_detail(
    post_id: int,
    db: AsyncSession = Depends(get_db)
):
    post, comment_rows = await forum.get_post_detail(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="帖子不存在")

    # 字典 + model_validate
    comments = [
        CommentItemResponse.model_validate({
            "commentId": cid,
            "username": name,
            "content": content,
            "createdAt": ctime
        })
        for cid, name, content, ctime in comment_rows
    ]

    data = PostDetailResponse.model_validate({
        "postId": post.id,
        "title": post.title,
        "content": post.content,
        "viewCount": post.view_count,
        "createdAt": post.created_at,
        "comments": comments
    })

    return success_response(data=data)

# ==================== 发布评论 ====================
@router.post("/comment")
async def create_comment(
    req: CreateCommentRequest,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    await forum.create_comment(db, user.id, req.post_id, req.content)
    return success_response(message="评论成功")

# ==================== 删除自己的帖子 ====================
@router.delete("/post/{post_id}")
async def delete_post(
    post_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    ok = await forum.delete_post(db, post_id, user.id)
    if not ok:
        raise HTTPException(status_code=403, detail="只能删除自己的帖子")
    return success_response(message="删除成功")

# ==================== 删除自己的评论 ====================
@router.delete("/comment/{comment_id}")
async def delete_comment(
    comment_id: int,
    user: User = Depends(get_current_token),
    db: AsyncSession = Depends(get_db)
):
    ok = await forum.delete_comment(db, comment_id, user.id)
    if not ok:
        raise HTTPException(status_code=403, detail="只能删除自己的评论")
    return success_response(message="删除成功")