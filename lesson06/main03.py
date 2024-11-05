"""
Задание №6
Необходимо создать базу данных для интернет-магазина. База данных должна
состоять из трех таблиц: товары, заказы и пользователи. Таблица товары должна
содержать информацию о доступных товарах, их описаниях и ценах. Таблица
пользователи должна содержать информацию о зарегистрированных
пользователях магазина. Таблица заказы должна содержать информацию о
заказах, сделанных пользователями.
    ○ Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY),
    имя, фамилия, адрес электронной почты и пароль.
    ○ Таблица товаров должна содержать следующие поля: id (PRIMARY KEY),
    название, описание и цена.
    ○ Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id
    пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус
    заказа.

Задание №6 (продолжение)
Создайте модели pydantic для получения новых данных и
возврата существующих в БД для каждой из трёх таблиц
(итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через
создание маршрутов, REST API (итого 15 маршрутов).
    ○ Чтение всех
    ○ Чтение одного
    ○ Запись
    ○ Изменение
    ○ Удаление
"""
import databases
import sqlalchemy
from fastapi import FastAPI
from lesson06.model03 import UserIn, User, Product, ProductIn, Order, OrderIn
from typing import List
from contextlib import asynccontextmanager
from faker import Faker

DATA_BASE_URL = "sqlite:///online_shop.db"

db = databases.Database(DATA_BASE_URL)

metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table('users',
                         metadata,
                         sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column('first_name', sqlalchemy.String(30)),
                         sqlalchemy.Column('last_name', sqlalchemy.String(30)),
                         sqlalchemy.Column('email', sqlalchemy.String(50)),
                         sqlalchemy.Column('password', sqlalchemy.String(30)),
                         )

products = sqlalchemy.Table('products',
                            metadata,
                            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column('name', sqlalchemy.String(30)),
                            sqlalchemy.Column('description', sqlalchemy.String(255)),
                            sqlalchemy.Column('price', sqlalchemy.Float)
                            )

orders = sqlalchemy.Table('orders',
                          metadata,
                          sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column('user_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column('product_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column('order_date', sqlalchemy.DateTime()),
                          sqlalchemy.Column('status', sqlalchemy.String(20))
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


@app.get("/users/{count}")
async def fill_user_table(count: int):
    for i in range(count):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()
        password = fake.unique.password()
        query = users.insert().values(first_name=first_name,
                                      last_name=last_name,
                                      email=email,
                                      password=password
                                      )
        await db.execute(query)
    return {'message': 'Users are created successfully'}


@app.get("/products/{count}")
async def fill_product_table(count: int):
    for i in range(count):
        name = fake.word()
        description = ' '.join(fake.words(nb=10))
        price = fake.random_int(min=100, max=1000)
        query = products.insert().values(name=name,
                                         description=description,
                                         price=price,
                                         )
        await db.execute(query)
    return {'message': 'Products are created successfully'}


@app.get("/orders/{count}")
async def fill_order_table(count: int):
    for i in range(count):
        user_id = fake.random_int(min=1, max=10)
        product_id = fake.random_int(min=1, max=10)
        order_date = fake.date_time_between(start_date='-30d', end_date='now')
        status = fake.random_element(elements=['новый', 'выполнен', 'отменен'])
        query = orders.insert().values(user_id=user_id,
                                       product_id=product_id,
                                       order_date=order_date,
                                       status=status
                                       )
        await db.execute(query)
    return {'message': 'Products are created successfully'}


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


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_record_id = await db.execute(query)
    return {**product.model_dump(), "id": last_record_id}


@app.get("/products/", response_model=List[Product])
async def get_products():
    query = products.select()
    return await db.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await db.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product_update: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**product_update.model_dump())
    await db.execute(query)
    return {**product_update.model_dump(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await db.execute(query)
    return {"message": "Product deleted"}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await db.execute(query)
    return {**order.model_dump(), "id": last_record_id}


@app.get("/orders/", response_model=List[Order])
async def get_orders():
    query = orders.select()
    return await db.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await db.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order_update: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**order_update.model_dump())
    await db.execute(query)
    return {**order_update.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await db.execute(query)
    return {"message": "Order deleted"}
