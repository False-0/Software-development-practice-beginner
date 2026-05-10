from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import QuestionItemBase

# ===================== 错题响应 =====================
class ErrorItemResponse(QuestionItemBase):
    error_id: int = Field(alias="errorId")
    wrong_count: int = Field(alias="wrongCount")
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class ErrorListResponse(BaseModel):
    list: list[ErrorItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class ErrorStatisticsResponse(BaseModel):
    total_error_count: int = Field(alias="totalErrorCount")
    today_error_count: int = Field(alias="todayErrorCount")
    top_chapter_id: int = Field(alias="topChapterId")
    top_chapter_num: int = Field(alias="topChapterNum")

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)


# ===================== 错题章节分布（折线图用） =====================
class ChapterErrorItem(BaseModel):
    chapter_name: str = Field(alias="chapterName")
    count: int

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)

class ChapterErrorDistributionResponse(BaseModel):
    list: list[ChapterErrorItem]

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)