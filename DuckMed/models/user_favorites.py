from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from models.questions import Questions
from models.users import User

class Base(DeclarativeBase):
    pass

# ===================== 用户题目收藏表 =====================
class UserFavorites(Base):
    __tablename__ = 'user_favorites'

    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='uk_user_question'),
        Index('idx_user_id', 'user_id'),
        Index('idx_question_id', 'question_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="收藏ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    question_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="收藏的题目ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserFavorites(id={self.id}, user_id={self.user_id}, question_id={self.question_id})>"