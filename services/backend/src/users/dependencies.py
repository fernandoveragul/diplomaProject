from typing import Generator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_async_session
from src.users.models import user
from src.users.schemas import User


class DUsers:
    @staticmethod
    async def get_all(session: AsyncSession = Depends(get_async_session)) -> list[User]:
        dt = await session.execute(select(user.c.email_user, user.c.registered_at))
        returned_dt = [User.from_orm(usr) for usr in dt.all()]
        return returned_dt

    @staticmethod
    async def get_cur(*, email_user: str, session: AsyncSession = Depends(get_async_session)) -> User:
        dt = await session.execute(
            select(user.c.email_user, user.c.registered_at).where(user.c.email_user == email_user)
        )
        return User.from_orm(dt.first())
