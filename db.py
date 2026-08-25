import sqlite3


def init_db():
    conn = sqlite3.connect("todo.db")
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()


def get_todo(todo_id):
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, content, done FROM todos WHERE id=?", [todo_id]
        )
        row = cursor.fetchone()
        if row is None:
            return {"todo": None}
        return {"todo": row}
    finally:
        conn.close()


def get_todos():
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, done FROM todos ORDER BY id DESC")
        rows = cursor.fetchall()
        return rows
    finally:
        conn.close()


def create_todo(title, content):
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO todos (title, content) VALUES (?, ?)", (title, content)
        )
        conn.commit()
        return {"last_inserted_id": cursor.lastrowid}
    finally:
        conn.close()

