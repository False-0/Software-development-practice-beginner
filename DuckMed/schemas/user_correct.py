from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from schemas.base import QuestionItemBase

# ===================== 做对题目响应 =====================
class CorrectItemResponse(QuestionItemBase):
    correct_id: int = Field(alias="correctId")
    created_at: datetime = Field(alias="createdAt")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )


class CorrectListResponse(BaseModel):
    list: list[CorrectItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )
