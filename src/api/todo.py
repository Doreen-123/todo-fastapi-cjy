from fastapi import HTTPException, APIRouter, status
from src.controllers import todo_controller
from src.schemas.todo import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post(
    "", response_model=TodoResponse, status_code=status.HTTP_201_CREATED
)
def create_todo(payload: TodoCreate):
    """建立一筆新的待辦事項 (回傳 201 Created)"""
    return todo_controller.create_todo(payload)

@router.get("", response_model=list[TodoResponse])
def get_all_todos():
    """取得所有待辦事項清單"""
    return todo_controller.get_all_todos()

@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo_by_id(todo_id: str):
    todo = todo_controller.get_todo_by_id(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {todo_id} 的待辦事項",
        )
    return todo

@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, payload: TodoUpdate):
    """更新指定 ID 的待辦事項"""
    updated_todo = todo_controller.update_todo(todo_id, payload)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {todo_id} 的待辦事項，無法更新",
        )
    return updated_todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: str):
    """刪除指定 ID 的待辦事項 (成功回傳 204 No Content)"""
    data = todo_controller.delete_todo(todo_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"找不到 ID 為 {todo_id} 的待辦事項，無法刪除",
        )
    return None
