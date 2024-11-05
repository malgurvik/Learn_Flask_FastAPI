"""
Задание №1.
Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.
    Создайте модуль приложения и настройте сервер и маршрутизацию.
    Создайте класс Task с полями id, title, description и status.
    Создайте список tasks для хранения задач.
    Создайте маршрут для получения списка задач (метод GET).
    Создайте маршрут для создания новой задачи (метод POST).
    Создайте маршрут для обновления задачи (метод PUT).
    Создайте маршрут для удаления задачи (метод DELETE).
    Реализуйте валидацию данных запроса и ответа.
"""

from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


tasks = []

for i in range(1, 11):
    tasks.append(Task(id=i,
                      title=f"Task {i}",
                      description=f"Description {i}",
                      status=random.choice(["Active", "Inactive"]))
                 )


@app.get("/")
async def root():
    return {"message": "Hello Malgurvik"}


@app.get("/tasks")
async def get_tasks():
    return tasks


@app.post("/tasks")
async def create_task(task: Task):
    tasks.append(task)
    return task


@app.put("/tasks")
async def update_task(task_id: int, task: Task):
    for t in tasks:
        if t.id == task_id:
            t.title = task.title
            t.description = task.description
            t.status = task.status
            return t
    return {"message": "Task not found"}


@app.delete("/tasks")
async def delete_task(task_id: int):
    for t in tasks:
        if t.id == task_id:
            tasks.remove(t)
            return {"message": "Task deleted"}
    return {"message": "Task not found"}
