import uuid

from typing import List
from pydantic import BaseModel
from datetime import datetime, date

from src.reviews.schemas import ReviewModel


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


class BookDetailModel(Book):
    reviews: List[ReviewModel]


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
