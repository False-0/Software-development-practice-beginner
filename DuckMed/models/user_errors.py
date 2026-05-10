from datetime import datetime
from sqlalchemy import Index, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.users import User
from models.questions import Questions, Subjects, Chapters

class Base(DeclarativeBase):
    pass


class UserError(Base):
    __tablename__ = 'user_errors'
    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='uk_user_question'),
        Index('idx_user_id', 'user_id'),
        Index('idx_question_id', 'question_id'),
        Index('idx_chapter_id', 'chapter_id'),
        Index('idx_subject_id', 'subject_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="错题ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")
    question_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="题目ID")
    subject_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="科目ID")
    chapter_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="章节ID")

    # 做错次数
    wrong_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False, comment="错误次数")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def __repr__(self):
        return f"<UserError(user_id={self.user_id}, question_id={self.question_id}, count={self.wrong_count})>"