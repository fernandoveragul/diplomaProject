from uuid import UUID

from fastapi import APIRouter, status

from src.news.schemas import Post

news_router = APIRouter(prefix="/news")


@news_router.get(path="/all", status_code=status.HTTP_200_OK, response_model=list[Post])
async def get_all_posts() -> list[Post]:
    ...


@news_router.post(path="/create", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    ...


@news_router.put(path="/update", status_code=status.HTTP_202_ACCEPTED)
async def update_post(uuid_post: UUID):
    ...


@news_router.delete(path="/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(uuid_post: UUID):
    ...
