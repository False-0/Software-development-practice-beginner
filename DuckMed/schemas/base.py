from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

# ===================== 试题基础=====================
class QuestionItemBase(BaseModel):
    id: int
    chapter_id: int = Field(alias="chapterId")
    title: str
    option_a: str = Field(alias="optionA")
    option_b: str = Field(alias="optionB")
    option_c: str = Field(alias="optionC")
    option_d: str = Field(alias="optionD")
    answer: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )