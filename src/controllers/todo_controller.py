# 加工與計算，整理好再交給 Repository 

import uuid
from typing import Optional
from datetime import datetime, timezone

from src.repositories import todo_repository
from src.schemas.todo import TodoCreate, TodoUpdate

def create_todo(payload: TodoCreate) -> dict:
    """補上系統欄位"""
    now = datetime.now(timezone.utc).isoformat()

    todo_data = {
        "id": str(uuid.uuid4()),
        "title": payload.title,
        "description": payload.description,
        "is_completed": False, # 預設未完成
        "priority": payload.priority.value,
        "due_date": payload.due_date,
        "created_at": now,
        "updated_at": now
    }

    return todo_repository.create_todo(todo_data)

def get_all_todos() -> list[dict]:
    return todo_repository.get_all_todos()

def get_todo_by_id(todo_id: str) -> Optional[dict]:
    return todo_repository.get_todo_by_id(todo_id)

def update_todo(todo_id: str, payload: TodoUpdate) -> Optional[dict]:
    # exclude_unset=True 會排除前端「沒有傳」的欄位，保留原本資料庫的值
    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        return todo_repository.get_todo_by_id(todo_id)
    
    # 如果有修改優先級 Enum，轉成字串
    if "priority" in update_data and update_data["priority"] is not None:
        update_data["priority"] = update_data["priority"].value

    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    return todo_repository.update_todo(todo_id, update_data)

def delete_todo(todo_id: str) -> bool:
    return todo_repository.delete_todo(todo_id)