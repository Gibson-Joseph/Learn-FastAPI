from typing import List

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.books.schemas import Book
from src.auth.dependencies import RoleChecker

from .service import TagService
from .schemas import TagAddModel, TageCreateModel, TagModel

tags_router = APIRouter()
tag_service = TagService()
user_role_checker = Depends(RoleChecker(["user", "admin"]))


@tags_router.get("/", response_model=List[TagModel], dependencies=[user_role_checker])
async def get_all_tags(session: AsyncSession = Depends(get_session)):
    tags = await tag_service.get_tags(session)

    return tags


@tags_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[user_role_checker],
    response_model=TagModel,
)
async def add_tag(
    tag_data: TageCreateModel, session: AsyncSession = Depends(get_session)
):
    tag_added = await tag_service.add_tag(tag_data, session)
    return tag_added


@tags_router.post(
    "/book/{book_uid}/tags", response_model=Book, dependencies=[user_role_checker]
)
async def add_tags_to_book(
    book_uid: str,
    tag_data: TagAddModel,
    session: AsyncSession = Depends(get_session),
):
    book_with_tag = await tag_service.add_tags_to_books(book_uid, tag_data, session)

    return book_with_tag


@tags_router.put(
    "/{tag_uid}", response_model=TagModel, dependencies=[user_role_checker]
)
async def update_tag(
    tag_uid: str,
    tag_update_data: TageCreateModel,
    session: AsyncSession = Depends(get_session),
):
    updated_tag = await tag_service.update_tag(tag_uid, tag_update_data, session)

    return updated_tag


@tags_router.delete(
    "/{tag_uid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[user_role_checker],
)
async def delete_tag(tag_uid: str, session: AsyncSession = Depends(get_session)):
    updated_tag = await tag_service.delete_tag(tag_uid, session)

    return updated_tag
