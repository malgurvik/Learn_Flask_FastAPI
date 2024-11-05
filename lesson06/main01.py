"""
Задание №1
    - Разработать API для управления списком пользователей с
    использованием базы данных SQLite. Для этого создайте
    модель User со следующими полями:
        ○ id: int (идентификатор пользователя, генерируется
        автоматически)
        ○ username: str (имя пользователя)
        ○ email: str (электронная почта пользователя)
        ○ password: str (пароль пользователя)
Задание №1 (продолжение)
    - API должно поддерживать следующие операции:
        ○ Получение списка всех пользователей: GET /users/
        ○ Получение информации о конкретном пользователе: GET /users/{user_id}/
        ○ Создание нового пользователя: POST /users/
        ○ Обновление информации о пользователе: PUT /users/{user_id}/
        ○ Удаление пользователя: DELETE /users/{user_id}/
    - Для валидации данных используйте параметры Field модели User.
    - Для работы с базой данных используйте SQLAlchemy и модуль databases.
"""
# from random import randint

import databases
import sqlalchemy
from fastapi import FastAPI
from lesson06.model01 import UserIn, User
from typing import List
from contextlib import asynccontextmanager

DATA_BASE_URL = "sqlite:///users.db"

db = databases.Database(DATA_BASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('username', sqlalchemy.String(30)),
                         sqlalchemy.Column('email', sqlalchemy.String(50)),
                         sqlalchemy.Column('password', sqlalchemy.String(30))
                         )

engine = sqlalchemy.create_engine(DATA_BASE_URL, connect_args={'check_same_thread': False})

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()


app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup():
#     await db.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await db.disconnect()
# @app.get("/users/{count}")
# async def fill_db(count: int):
#     for i in range(2, count):
#         query = users.insert().values(username=f'user{i}',
#                                       email=f'mail{i}@mail.ru',
#                                       password=f'{randint(10000000, 99999999)}')
#         await db.execute(query)
#     return {'message': 'Users are created successfully'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(username=user.username, email=user.email, password=user.password)
    last_record_id = await db.execute(query)
    return {**user.model_dump(), "id": last_record_id}

@app.get("/users/", response_model=List[User])
async def get_users():
    query = users.select()
    return await db.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await db.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserIn):
    query = users.update().where(users.c.id == user_id).values(**user_update.model_dump())
    await db.execute(query)
    return {**user_update.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await db.execute(query)
    return {"message": "User deleted"}
