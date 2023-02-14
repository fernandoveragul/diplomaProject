from fastapi import APIRouter, status
from src.users.dependencies import DUsers
from src.users.schemas import User

news_router = APIRouter(prefix="/usr")


@news_router.get("/all", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_all_users():
    result = await DUsers.get_all()
    return result


@news_router.get("/current", status_code=status.HTTP_200_OK)
async def get_current_user():
    ...


@news_router.post("/create")
async def create_user():
    ...


@news_router.put("/update")
async def update_user():
    ...


@news_router.delete("/del")
async def delete_user():
    ...
