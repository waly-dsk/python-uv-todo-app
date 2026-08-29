from fastapi import FastAPI
from pydantic import BaseModel

from db import get_connection

app = FastAPI()


class TodoCreate(BaseModel):
    title: str
    content: str | None = None


@app.get("/healthz")
def health_check():
    return {"status": "OK"}


@app.get("/todos")
def get_todos():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM todos").fetchall()


@app.post("/todos")
def create_todo(todo: TodoCreate):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO todos (title, content) VALUES (%s, %s)",
            (todo.title, todo.content),
        )

    return {"status": "created"}
