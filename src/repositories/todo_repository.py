import sqlite3
from pathlib import Path

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