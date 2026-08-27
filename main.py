from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import db


class Todo(BaseModel):
    title: str
    content: str


class TodoDone(BaseModel):
    done: bool


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/healthz")
def health_check():
    return {"status": "ok"}


@app.get("/")
def welcome_route():
    return FileResponse("static/index.html")


@app.get("/get_todos")
def get_todos():
    todos = db.get_todos()
    return {"todos": todos}


@app.get("/get_todo/{todo_id}")
def get_todo(todo_id: int):
    result = db.get_todo(todo_id)
    if result["todo"] is None:
        raise HTTPException(status_code=404, detail="Todo introuvable")
    return result


@app.post("/create_todo")
def create_todo(todo: Todo):
    return db.create_todo(todo.title, todo.content)


@app.post("/update_todo/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    return db.update_todo(todo_id, todo.title, todo.content)


@app.post("/toggle_todo/{todo_id}")
def toggle_todo(todo_id: int, payload: TodoDone):
    return db.set_todo_done(todo_id, payload.done)


@app.post("/delete_todo/{todo_id}")
def delete_todo(todo_id: int):
    return db.delete_todo(todo_id)


# Serve static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
