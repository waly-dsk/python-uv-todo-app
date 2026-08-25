from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import db

app = FastAPI()


class Todo(BaseModel):
    title: str
    content: str


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


@app.post("/create_todo")
def create_todo(todo: Todo):
    last_inserted_id = db.create_todo(todo.title, todo.content)
    return {"last_inserted_id": last_inserted_id}


# Serve static files
app.mount("/static", StaticFiles(directory="static", html=True), name="static")
