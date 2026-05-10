from datetime import datetime
from sqlalchemy import Integer, String, Text, TIMESTAMP, Index
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from sqlalchemy.sql import func

class Base(DeclarativeBase):
    pass

# 帖子表
class ForumPosts(Base):
    __tablename__ = "forum_posts"
    __table_args__ = (
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="帖子ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="发布用户ID")
    title: Mapped[str] = mapped_column(String(200), nullable=False, comment="帖子标题")
    content: Mapped[str] = mapped_column(Text, nullable=False, comment="帖子内容")
    view_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="浏览量")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

# 评论表
class ForumComments(Base):
    __tablename__ = "forum_comments"
    __table_args__ = (
        Index("idx_post_id", "post_id"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="评论ID")
    post_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="所属帖子ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="评论用户ID")
    content: Mapped[str] = mapped_column(String(500), nullable=False, comment="评论内容")

    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())