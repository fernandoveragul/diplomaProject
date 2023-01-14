from datetime import datetime

from fastapi import APIRouter
from.schemas import Post

router = APIRouter(
    prefix="/post"
)

POSTS = [
    {
        "id": 1,
        "date": datetime.utcnow(),
        "author": "super",
        "text": "hello world",
        "images": ["/usr/post/images"],
    },
    {
        "id": 2,
        "date": datetime.utcnow(),
        "author": "usually",
        "text": "hello world",
        "images": ["/usr/post/images"],
    },
    {
        "id": 3,
        "date": datetime.utcnow(),
        "author": "ghost",
        "text": "hello world",
        "images": ["/usr/post/images"],
    },
]


@router.get("/", response_model=Post)
async def get_post_by_id(*, post_id: int = None) -> dict:
    for post in POSTS:
        if post_id == post.get("id"):
            return post

