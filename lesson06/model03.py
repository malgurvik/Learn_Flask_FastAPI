from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    email: EmailStr = Field(max_length=50)
    password: str = Field(min_length=8)


class User(UserIn):
    id: int

class ProductIn(BaseModel):
    name: str = Field(min_length=2)
    description: str = Field(min_length=10)
    price: float = Field(gt=0)

class Product(ProductIn):
    id: int

class OrderIn(BaseModel):
    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    date: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d - %H:%M:%S'))
    status: str = Field()

class Order(OrderIn):
    id: int




