from pydantic import BaseModel, ConfigDict, Field
from typing import List

class Top3Item(BaseModel):
    username: str
    total_done: int = Field(alias="totalDone")

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)

class RankInfoResponse(BaseModel):
    my_rank: int = Field(alias="myRank")
    total_done: int = Field(alias="totalDone")
    total_correct: int = Field(alias="totalCorrect")
    correct_rate: float = Field(alias="correctRate")
    top3: List[Top3Item] = Field(alias="top3")

    model_config = ConfigDict(populate_by_name=True,from_attributes=True)