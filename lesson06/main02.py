"""
Задание №2.
Создать веб-приложение на FastAPI, которое будет предоставлять API для
работы с базой данных пользователей. Пользователь должен иметь
следующие поля:
    ○ ID (автоматически генерируется при создании пользователя)
    ○ Имя (строка, не менее 2 символов)
    ○ Фамилия (строка, не менее 2 символов)
    ○ Дата рождения (строка в формате "YYYY-MM-DD")
    ○ Email (строка, валидный email)
    ○ Адрес (строка, не менее 5 символов)

Задание №2 (продолжение)
API должен поддерживать следующие операции:
    ○ Добавление пользователя в базу данных
    ○ Получение списка всех пользователей в базе данных
    ○ Получение пользователя по ID
    ○ Обновление пользователя по ID
    ○ Удаление пользователя по ID
Приложение должно использовать базу данных SQLite3 для хранения
пользователей.
"""

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from lesson06.model02 import UserIn, User
from typing import List
from contextlib import asynccontextmanager
from faker import Faker

DATA_BASE_URL = "sqlite:///users2.db"

db = databases.Database(DATA_BASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('first_name', sqlalchemy.String(30)),
                         sqlalchemy.Column('last_name', sqlalchemy.String(30)),
                         sqlalchemy.Column('birth_date', sqlalchemy.Date()),
                         sqlalchemy.Column('email', sqlalchemy.String(50)),
                         sqlalchemy.Column('address', sqlalchemy.String(30))
                         )

engine = sqlalchemy.create_engine(DATA_BASE_URL, connect_args={'check_same_thread': False})

metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconnect()

fake = Faker('ru_RU')

app = FastAPI(lifespan=lifespan)



# @app.get("/users/{count}")
# async def fill_db(count: int):
#     for i in range(count):
#         first_name = fake.first_name()
#         last_name = fake.last_name()
#         birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)
#         email = fake.unique.email()
#         address = fake.address()
#         query = users.insert().values(first_name=first_name,
#                                       last_name=last_name,
#                                       birth_date=birth_date,
#                                       email=email,
#                                       address=address
#                                       )
#         await db.execute(query)
#     return {'message': 'Users are created successfully'}


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
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


if __name__ == '__main__':
    uvicorn.run("main02:app", port=8000, reload=True)