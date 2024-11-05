from pydantic import BaseModel, Field


class UserIn(BaseModel):
    username: str = Field(max_length=30)
    email: str = Field(max_length=50)
    password: str = Field(min_length=8, max_length=30)

class User(UserIn):
    id: int