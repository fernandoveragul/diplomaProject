from fastapi import APIRouter, status

from src.news.schemas import News

news_router = APIRouter(prefix="/nws")


@news_router.get("/", response_model=list[News])
async def get_all_news_posts():
    ...


@news_router.get("/{post_data}")
async def get_single_news_post(*, post_data):
    ...


@news_router.post("/")
async def create_new_news_post():
    ...


@news_router.post("/{post_data}")
async def change_exist_news_post(*, post_data):
    ...


@news_router.delete("/{post_data}")
async def delete_exist_news_post(*, post_data):
    ...
