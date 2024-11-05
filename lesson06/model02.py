from datetime import date

from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    first_name: str = Field(min_length=2)
    last_name: str = Field(min_length=2)
    birth_date: date = Field()
    email: EmailStr = Field(max_length=50)
    address: str = Field(min_length=5)


class User(UserIn):
    id: int
