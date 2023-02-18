from typing import Any
from uuid import UUID

from fastapi import APIRouter, status, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, insert, update, delete, ScalarResult

from src.database import get_async_session
from src.news.models import post
from src.news.schemas import Post

news_router = APIRouter(prefix="/news")


@news_router.get(path="/", status_code=status.HTTP_200_OK, response_model=list[Post])
async def get_all_posts(session: AsyncSession = Depends(get_async_session)) -> list[Post]:
    result = await session.execute(select(post))
    lst = [Post.from_orm(i) for i in result.fetchall()]
    return lst


@news_router.get(path="/{id_post}", status_code=status.HTTP_200_OK, response_model=Post | dict)
async def get_post(id_post: UUID | None = Path(default=...),
                   session: AsyncSession = Depends(get_async_session)) -> Post | dict:
    if not id_post:
        return {"detail": "have not post"}
    result = await session.execute(select(post).where(post.c.uuid_post == id_post))
    return Post.from_orm(result.first())


@news_router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create_post(cur_post: Post, session: AsyncSession = Depends(get_async_session)) -> None:
    await session.execute(insert(post).values(**cur_post.dict()))
    await session.commit()


@news_router.put(path="/", status_code=status.HTTP_202_ACCEPTED)
async def update_post(replacement: Post, uuid_post: UUID, session: AsyncSession = Depends(get_async_session)):
    await session.execute(update(post).values(**replacement.dict()).where(post.c.uuid_post == uuid_post))
    await session.commit()


@news_router.delete(path="/", status_code=status.HTTP_202_ACCEPTED)
async def delete_post(uuid_post: UUID, session: AsyncSession = Depends(get_async_session)):
    await session.execute(delete(post).where(post.c.uuid_post == uuid_post))
    await session.commit()
