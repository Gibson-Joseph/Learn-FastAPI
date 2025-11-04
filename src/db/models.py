import uuid
import sqlalchemy.dialects.postgresql as pg

from typing import List, Optional
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, date


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
    books: List["Book"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin"},  # Could not understand
    )
    # A Relationship() defines how Python objects (models) are connected — not how the foreign keys exist in the database (that’s done by Field(..., foreign_key="...")).
    # “When I load a User, also let me access all the Book objects related to it.”

    reviews: List["Review"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    # Why are some class names in quotes (like "Book", "Review")?
    # That’s called a forward reference — needed when Python encounters a class name before it’s defined.

    # At this moment, Python hasn’t seen the Book class yet — it will be defined below.
    # If you wrote books: List[Book] here, Python would raise a NameError because Book isn’t defined yet.

    # By writing "Book" as a string, you’re telling Python:
    # “This refers to a class that will exist later.”
    def __repr__(self):
        return f"<User {self.username}>"


class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Book(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4),
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # Reverse Relationship
    # Reverse link back to the users
    # https://sqlmodel.tiangolo.com/tutorial/relationship-attributes/back-populates/
    user: Optional[User] = Relationship(back_populates="books")  # Could not understand
    # “When I load a Book, I can see which User owns it.”
    reviews: List["Review"] = Relationship(
        back_populates="book", sa_relationship_kwargs={"lazy": "selectin"}
    )

    tags: List["Tag"] = Relationship(
        link_model=BookTag,
        back_populates="books",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4),
    )
    rating: int = Field(le=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    book_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="books.uid")
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    # https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html#summary-of-relationship-loading-styles
    user: Optional[User] = Relationship(
        back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"}
    )
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"


class Tag(SQLModel, table=True):
    __tablename__ = "tags"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List[Book] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
