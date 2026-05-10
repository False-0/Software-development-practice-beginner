from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List

class PostItemResponse(BaseModel):
    post_id: int = Field(alias="postId")
    title: str
    view_count: int = Field(alias="viewCount")
    created_at: datetime = Field(alias="createdAt")
    model_config = ConfigDict(populate_by_name=True)

class PostListResponse(BaseModel):
    list: List[PostItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")
    model_config = ConfigDict(populate_by_name=True)

class HotPostItemResponse(BaseModel):
    post_id: int = Field(alias="postId")
    title: str
    view_count: int = Field(alias="viewCount")
    model_config = ConfigDict(populate_by_name=True)

class CommentItemResponse(BaseModel):
    comment_id: int = Field(alias="commentId")
    username: str
    content: str
    created_at: datetime = Field(alias="createdAt")
    model_config = ConfigDict(populate_by_name=True)

class PostDetailResponse(BaseModel):
    post_id: int = Field(alias="postId")
    title: str
    content: str
    view_count: int = Field(alias="viewCount")
    created_at: datetime = Field(alias="createdAt")
    comments: List[CommentItemResponse]
    model_config = ConfigDict(populate_by_name=True)

class CreatePostRequest(BaseModel):
    title: str
    content: str
    model_config = ConfigDict(populate_by_name=True)

class CreateCommentRequest(BaseModel):
    post_id: int = Field(alias="postId")
    content: str
    model_config = ConfigDict(populate_by_name=True)