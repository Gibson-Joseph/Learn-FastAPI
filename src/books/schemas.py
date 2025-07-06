from pydantic import BaseModel
from datetime import datetime, date
import uuid


class Book(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    language: str
    publisher: str
    page_count: int
    published_date: date
    created_at: datetime
    updated_at: datetime


class BookCreateModel(BaseModel):
    title: str
    author: str
    language: str
    publisher: str
    page_count: int
    published_date: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    language: str
    publisher: str
    page_count: int
