from datetime import datetime
from sqlalchemy import Integer, String, Index, Text, ForeignKey, DateTime
from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    """基础模型：所有表共用创建时间、更新时间字段"""
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

# ===================== 科目表 =====================
class Subjects(Base):
    __tablename__ = 'subjects'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="科目ID")
    name: Mapped[str] = mapped_column(String(50), nullable=False, comment="科目名称：内科、外科等")

    def __repr__(self):
        return f"<Subjects(id={self.id}, name={self.name})>"

# ===================== 章节表 =====================
class Chapters(Base):
    __tablename__ = 'chapters'

    # 数据库索引：提升按科目查询速度
    __table_args__ = (
        Index('idx_subject_id', 'subject_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="章节ID")
    subject_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('subjects.id'),
        nullable=False,
        comment="所属科目ID"
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="章节名称")

    def __repr__(self):
        return f"<Chapters(id={self.id}, subject_id={self.subject_id}, name={self.name})>"

# ===================== 试题表 =====================
class Questions(Base):
    __tablename__ = 'questions'

    # 数据库索引：提升按章节查询速度
    __table_args__ = (
        Index('idx_chapter_id', 'chapter_id'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="试题ID")
    chapter_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('chapters.id'),
        nullable=False,
        comment="所属章节ID"
    )
    title: Mapped[str] = mapped_column(Text, nullable=False, comment="题干")
    option_a: Mapped[str] = mapped_column(Text, nullable=False, comment="选项A")
    option_b: Mapped[str] = mapped_column(Text, nullable=False, comment="选项B")
    option_c: Mapped[str] = mapped_column(Text, nullable=False, comment="选项C")
    option_d: Mapped[str] = mapped_column(Text, nullable=False, comment="选项D")
    answer: Mapped[str] = mapped_column(String(1), nullable=False, comment="正确答案：A/B/C/D")

    def __repr__(self):
        return f"<Questions(id={self.id}, chapter_id={self.chapter_id}, title={self.title[:20]}...)>"