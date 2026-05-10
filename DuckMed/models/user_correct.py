from datetime import datetime
from sqlalchemy import Index, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from models.users import User
from models.questions import Questions, Subjects, Chapters

class Base(DeclarativeBase):
    pass

class UserCorrect(Base):
    __tablename__ = 'user_correct'
    __table_args__ = (
        # 唯一键：一个用户只能对同一道题记一次正确
        UniqueConstraint('user_id', 'question_id', name='uk_user_question'),
        # 普通索引
        Index('idx_user_id', 'user_id'),
        Index('idx_chapter_id', 'chapter_id'),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(User.id),
        nullable=False,
        comment="用户ID"
    )
    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Questions.id),
        nullable=False,
        comment="做对的题目ID"
    )
    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Subjects.id),
        nullable=False,
        comment="科目ID"
    )
    chapter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Chapters.id),
        nullable=False,
        comment="章节ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        comment="做对时间"
    )

    def __repr__(self):
        return f"<UserCorrect(id={self.id}, user_id={self.user_id}, question_id={self.question_id})>"