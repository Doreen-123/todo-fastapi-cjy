# 寫規格的，把原有文字轉成 Code

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="代辦事項標題")
    description: Optional[str] = Field(default=None, description="詳細說明代辦事項")
    priority: PriorityEnum = Field(
        default=PriorityEnum.medium, description="事項優先級"
    )
    due_date: Optional[str] = Field(default=None, min_length=1,max_length=30, description="截止時間")

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100, description="修改標題")
    description: Optional[str] = Field(default=None, description="修改詳細說明")
    is_completed: Optional[bool] = Field(default=None, description="修改完整狀態")
    priority: Optional[PriorityEnum] = Field(default=None, description="修改優先級")
    due_date: Optional[str] = Field(default=None, description="修改截止時間")

class TodoResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    is_completed: bool
    priority: PriorityEnum
    due_date: Optional[str]
    created_at: str
    updated_at: str
