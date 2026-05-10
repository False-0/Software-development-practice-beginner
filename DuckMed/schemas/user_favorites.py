from datetime import datetime

from pydantic import BaseModel,Field,ConfigDict

from schemas.base import QuestionItemBase

# ===================== 题目收藏 =====================
class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias="isFavorite")

class FavoriteAddRequest(BaseModel):
    question_id: int = Field(..., alias="questionId")

class FavoriteQuestionItemResponse(QuestionItemBase):
    favorite_id: int = Field(alias="favoriteId")
    favorite_time: datetime = Field(alias="favoriteTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class FavoriteListResponse(BaseModel):
    list: list[FavoriteQuestionItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )