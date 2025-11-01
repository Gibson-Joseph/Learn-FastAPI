import uuid
import sqlalchemy.dialects.postgresql as pg

from typing import List
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime

from src.books import models


class User(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(pg.VARCHAR, server_default="user")
    )  # server_default like telling PostgreSQL: “For this new column, use this default for all old rows too.”
    is_verified: bool = Field(default=False)
    password_hash: str = Field(exclude=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Reverse Relationship
    # Reverse link back to the books
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/
    books: List["models.Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},  # Could not understand
    )

    def __repr__(self):
        return f"<User {self.username}>"
