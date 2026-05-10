from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, delete
from models.forum import ForumPosts, ForumComments
from models.users import User

# ==================== 1. 获取全部帖子（分页） ====================
async def get_post_list(
    db: AsyncSession,
    page: int = 1,
    page_size: int = 10
):
    count_query = select(func.count(ForumPosts.id))
    total = await db.scalar(count_query) or 0

    offset = (page - 1) * page_size
    query = (
        select(ForumPosts)
        .order_by(desc(ForumPosts.created_at))
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.scalars().all()
    return rows, total

# ==================== 2. 热门帖子 TOP10 ====================
async def get_hot_posts(db: AsyncSession, limit: int = 10):
    query = (
        select(ForumPosts)
        .order_by(desc(ForumPosts.view_count))
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()

# ==================== 3. 发布帖子 ====================
async def create_post(db: AsyncSession, user_id: int, title: str, content: str):
    post = ForumPosts(
        user_id=user_id,
        title=title,
        content=content
    )
    db.add(post)
    await db.commit()

# ==================== 4. 帖子详情 + 评论列表 ====================
async def get_post_detail(db: AsyncSession, post_id: int):
    # 查询帖子
    post_query = select(ForumPosts).where(ForumPosts.id == post_id)
    post = await db.scalar(post_query)
    if not post:
        return None, None

    # 浏览量 +1
    post.view_count += 1
    await db.commit()
    await db.refresh(post)

    comment_query = (
        select(
            ForumComments.id,
            User.username,
            ForumComments.content,
            ForumComments.created_at
        )
        .join(User)
        .where(ForumComments.post_id == post_id)
        .order_by(ForumComments.created_at.desc())
    )
    res = await db.execute(comment_query)
    comment_rows = res.all()

    return post, comment_rows

# ==================== 5. 发布评论 ====================
async def create_comment(db: AsyncSession, user_id: int, post_id: int, content: str):
    comment = ForumComments(
        user_id=user_id,
        post_id=post_id,
        content=content
    )
    db.add(comment)
    await db.commit()

# ==================== 6. 删除自己的帖子 ====================
async def delete_post(db: AsyncSession, post_id: int, user_id: int):
    query = select(ForumPosts).where(
        ForumPosts.id == post_id,
        ForumPosts.user_id == user_id
    )
    post = await db.scalar(query)
    if not post:
        return False

    await db.delete(post)
    await db.commit()
    return True

# ==================== 7. 删除自己的评论 ====================
async def delete_comment(db: AsyncSession, comment_id: int, user_id: int):
    query = select(ForumComments).where(
        ForumComments.id == comment_id,
        ForumComments.user_id == user_id
    )
    comment = await db.scalar(query)
    if not comment:
        return False

    await db.delete(comment)
    await db.commit()
    return True