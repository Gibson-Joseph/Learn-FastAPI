from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.books.service import BookService
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker


book_router = APIRouter()
book_service = BookService()
role_checker = Depends(RoleChecker(["admin", "user"]))
access_bearer = AccessTokenBearer()


@book_router.get(
    "/", response_model=List[Book], dependencies=[role_checker]
)  # FastAPI, please run this dependency function, but I don’t care about its return value
async def get_all_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
    # _:bool = Depends(role_checker)
):
    # “FastAPI, before running this endpoint, call these dependency functions. Whatever they return, inject that value into these parameters.”
    books = await book_service.get_all_books(session)
    return books


@book_router.get(
    "/user/{user_uid}", response_model=List[Book], dependencies=[role_checker]
)
async def get_user_book_submissions(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
):
    books = await book_service.get_user_books(user_uid, session)
    return books


@book_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
    dependencies=[role_checker],
)
async def create_a_book(
    book_data: BookCreateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
) -> dict:
    user_id = token_details.get("user")["user_uid"]
    new_book = await book_service.create_book(book_data, user_id, session)

    return new_book


@book_router.get(
    "/{book_uid}",
    dependencies=[role_checker],
    response_model=Book,
)
async def get_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
) -> Book:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )


@book_router.patch(
    "/{book_uid}",
    dependencies=[role_checker],
    response_model=Book,
)
async def update_book(
    book_uid: str,
    book_update_data: BookUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
) -> Book:
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return updated_book


@book_router.delete(
    "/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker]
)
async def delete_book(
    book_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_bearer),
):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    else:
        return {}
