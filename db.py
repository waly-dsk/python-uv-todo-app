import sqlite3


def init_db():
    conn = sqlite3.connect("todo.db")
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                done INTEGER NOT NULL DEFAULT 0
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


def update_todo(todo_id, title, content):
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET title=?, content=? WHERE id=?",
            (title, content, todo_id),
        )
        conn.commit()
        return {"updated_rows": cursor.rowcount}
    finally:
        conn.close()


def set_todo_done(todo_id, done):
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET done=? WHERE id=?", (1 if done else 0, todo_id)
        )
        conn.commit()
        return {"updated_rows": cursor.rowcount}
    finally:
        conn.close()


def delete_todo(todo_id):
    conn = sqlite3.connect("todo.db")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id=?", (todo_id,))
        conn.commit()
        return {"deleted_rows": cursor.rowcount}
    finally:
        conn.close()
