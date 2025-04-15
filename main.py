from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://todolisttify.netlify.app"],  # Replace "*" with your frontend domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_db = []


class Task(BaseModel):
    title: str
    details: str


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    if task_id >= len(tasks_db):
        return {"error": "Task not found"}
    tasks_db[task_id] = task
    return task

@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    if task_id >= len(tasks_db):
        return {"error": "Task not found"}
    deleted_task = tasks_db.pop(task_id)
    return deleted_task
