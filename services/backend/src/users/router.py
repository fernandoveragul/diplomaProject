import json

from fastapi import APIRouter, Depends, Body, status, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import DTokenGuard
from src.database import get_async_session
from src.users.models import MUser, MRoleUser
from src.users.schemas import SUserAD, SUser, SRoleDB, SUserDB, SRole

guarder = DTokenGuard()

user_router = APIRouter(prefix="/usr", dependencies=[Depends(guarder)])


@user_router.get("/",
                 status_code=status.HTTP_200_OK,
                 response_model=list[SUser],
                 summary="Endpoint return list all users")
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MUser))
    result = [SUserDB(user) for user in response.all()]
    return result


@user_router.get("/single",
                 status_code=status.HTTP_200_OK,
                 response_model=SUserAD,
                 summary="Endpoint return info about single user")
async def get_more_info_user(user_data: SUser = Body(..., alias="userData"),
                             session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MUser).where(MUser.email_user == user_data.email_user))
    if result := response.first():
        return SUserDB(result)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Can't find user with email: {user_data.email_user}")


@user_router.post("/create",
                  status_code=status.HTTP_201_CREATED,
                  response_model=SUserAD,
                  summary="Endpoint create new user")
async def create_new_user(user_data: SUserAD = Body(..., alias="userData"),
                          session: AsyncSession = Depends(get_async_session)):
    data = SUserDB(**user_data.dict())
    try:
        await session.execute(insert(MUser).values(**data.dict()))
        await session.commit()
        return data
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(user_data.dict(), indent=4)}")


@user_router.post("/update",
                  status_code=status.HTTP_202_ACCEPTED,
                  response_model=SUserAD,
                  summary="Endpoint change exist user")
async def change_exist_user(user_data: SUser = Body(..., alias="userData"),
                            session: AsyncSession = Depends(get_async_session)):
    data = SUserDB(**user_data.dict())
    response = await session.execute(select(MUser).where(MUser.email_user == user_data.email_user))
    if response.first():
        await session.execute(update(MUser).values(**data.dict()))
        await session.commit()
        return data
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(user_data.dict(), indent=4)}")


@user_router.delete("/delete",
                    status_code=status.HTTP_202_ACCEPTED,
                    response_model=SUser,
                    summary="Endpoint delete exist user")
async def delete_exist_user(user_data: SUser = Body(..., alias="userData"),
                            session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(MUser).where(MUser.email_user == user_data.email_user))
        await session.commit()
        return user_data
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(user_data.dict(), indent=4)}")


#########
# Roles #
#########

@user_router.post("/role/create",
                  status_code=status.HTTP_202_ACCEPTED,
                  response_model=SRole,
                  summary="Endpoint create new role",
                  include_in_schema=True)
async def create_new_role(role: SRole = Body(...),
                          permissions: list[str] = Body(..., embed=True),
                          session: AsyncSession = Depends(get_async_session)):
    data = SRoleDB(**role.dict(), permissions=permissions)
    try:
        await session.execute(insert(MRoleUser).values(**data.dict()))
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(data.dict(), indent=4)}")


@user_router.post("/role/update",
                  status_code=status.HTTP_202_ACCEPTED,
                  response_model=SRole,
                  summary="Endpoint change exist role",
                  include_in_schema=True)
async def change_exist_role(role: SRole = Body(...),
                            permissions: list[str] = Body(...),
                            session: AsyncSession = Depends(get_async_session)):
    data = SRoleDB(**role.dict(), permissions=permissions)
    try:
        await session.execute(update(MRoleUser).values(**data.dict()))
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(data.dict(), indent=4)}")


@user_router.post("/role/delete",
                  status_code=status.HTTP_202_ACCEPTED,
                  response_model=SRole,
                  summary="Endpoint delete exist role",
                  include_in_schema=True)
async def change_exist_role(role: SRole = Body(...),
                            session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(MRoleUser).where(MRoleUser.role == role.role))
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(role.dict(), indent=4)}")
