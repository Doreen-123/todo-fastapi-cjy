# 跟資料庫打交道的地方，拿鑰匙開門進出的概念(CRUD 資料庫操作)

import sqlite3
from pathlib import Path
from typing import Optional

DB_DIR = Path("data")
DB_PATH = DB_DIR / "todo.db"

def get_connection():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = (sqlite3.Row) # 結果可以用 row["title"] 取值
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                is_completed INTEGER NOT NULL default 0,
                priority TEXT NOT NULL DEFAULT 'medium',
                due_date TEXT,
                created_at TEXT NOT NULL, 
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.commit()

def create_todo(todo_data: dict) -> dict:
    """將一筆新的待辦事項寫入資料庫"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO todos(
                id, title, description, is_completed, priority, due_date, created_at, updated_at
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    todo_data["id"],
                    todo_data["title"],
                    todo_data.get("description"),
                    1 if todo_data.get("is_completed") else 0,
                    todo_data["priority"],
                    todo_data.get("due_date"),
                    todo_data["created_at"],
                    todo_data["updated_at"]
                ),
        )
        conn.commit()
        return todo_data

def get_all_todos() -> list[dict]:
    """撈出資料庫裡所有的待辦事項"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

def get_todo_by_id(todo_id: str) -> Optional[dict]:
    """依照 todo_id 撈出單筆待辦事項"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def delete_todo(todo_id: str) -> bool:
    """依照 todo_id 刪除待辦事項，成功回傳 True，資料不存在回傳 False"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        return cursor.rowcount > 0

def update_todo(todo_id: str, update_fields: dict) -> Optional[dict]:
    """動態更新指定欄位，並更新 updated_at"""
    if not update_fields:
        return get_todo_by_id(todo_id)

    set_clauses = [] # 組裝 SET 子句
    values = []

    for key, value in update_fields.items():
        set_clauses.append(f"{key} = ?")

        if key == "is_completed" and value is not None:
            values.append(1 if value else 0)
        else:
            values.append(value)

    values.append(todo_id)

    sql = f"""
        UPDATE todos
        SET {', '.join(set_clauses)}
        WHERE id = ?
    """

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        conn.commit()

        if cursor.rowcount == 0:
            return None

    return get_todo_by_id(todo_id)