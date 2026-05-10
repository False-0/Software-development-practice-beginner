from datetime import datetime

from sqlalchemy import UniqueConstraint, Index, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass
# ===================== 用户刷题统计表 =====================
class UserStatistics(Base):
    __tablename__ = 'user_statistics'

    # 唯一索引：每个用户只有一条统计
    __table_args__ = (
        UniqueConstraint('user_id', name='user_id_UNIQUE'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="统计ID")
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="用户ID")

    # 做题数量统计
    total_done: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="总做题数")
    total_correct: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="总做对题数")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment="做题创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(),
        comment="做题更新时间")

    def __repr__(self):
        return f"<UserStatistics(user_id={self.user_id}, done={self.total_done}, correct={self.total_correct})>"