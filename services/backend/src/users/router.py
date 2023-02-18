import uuid
from uuid import UUID

from fastapi import APIRouter, status, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.users.dependencies import DUsers
from src.users.schemas import User

news_router = APIRouter(prefix="/users")


@news_router.get("/", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    result = await DUsers.get_all(session=session)
    return result


@news_router.get("/{id_user}", status_code=status.HTTP_200_OK, response_model=User)
async def get_current_user(*, id_user: UUID | None = Path(default=...)):
    ...


@news_router.post("/")
async def create_user():
    ...


@news_router.put("/")
async def update_user():
    ...


@news_router.delete("/")
async def delete_user():
    ...
