from uuid import UUID

from db import get_connection
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TodoCreate(BaseModel):
    title: str
    content: str | None


class TodoResponse(BaseModel):
    id: UUID
    title: str
    content: str | None
    done: bool


class TodoUpdate(BaseModel):
    title: str
    content: str | None
    done: bool


@app.get("/healthz")
def health_check():
    return {"status": "OK"}


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    with get_connection() as conn:
        result = conn.execute(
            """
            INSERT INTO todos (title, content)
            VALUES (%s, %s)
            RETURNING id, title, content, done
            """,
            (todo.title, todo.content),
        )
        created_todo = result.fetchone()

    return created_todo


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: str):
    with get_connection() as conn:
        result = conn.execute(
            """
            SELECT id, title, content, done FROM todos WHERE id = %s
            """,
            (todo_id,),
        )
        this_todo = result.fetchone()
    return this_todo


@app.get("/todos", response_model=list[TodoResponse])
def get_todos():
    with get_connection() as conn:
        result = conn.execute("SELECT * FROM todos")
        todos = result.fetchall()
    return todos


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: str, todo: TodoUpdate):
    with get_connection() as conn:
        result = conn.execute(
            """
            UPDATE todos
            SET title = %s, content = %s, done =  %s
            WHERE id = %s
            RETURNING id, title, content, done
            """,
            (todo.title, todo.content, todo.done, todo_id),
        )
        updated_todo = result.fetchone()
    return updated_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM todos WHERE id = %s
            """,
            (todo_id,),
        )

    return {"message": "Todo deleted"}
