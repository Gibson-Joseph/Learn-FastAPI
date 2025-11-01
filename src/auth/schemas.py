import uuid

from typing import List
from datetime import datetime
from pydantic import BaseModel, Field

from src.books.schemas import Book


class UserCreateModel(BaseModel):
    email: str = Field(max_length=40)
    username: str = Field(max_length=8)
    password: str = Field(min_length=6)
    last_name: str = Field(max_length=25)
    first_name: str = Field(max_length=25)


class UserModel(BaseModel):
    uid: uuid.UUID
    email: str
    books: List[Book]
    username: str
    last_name: str
    first_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)
