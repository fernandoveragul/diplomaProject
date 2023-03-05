from fastapi import APIRouter, Depends, Body
from pydantic import Field

from src.auth.dependencies import DTokenGuard
from src.users.schemas import UserAD, User, RoleDB

guarder = DTokenGuard()

user_router = APIRouter(prefix="/usr", dependencies=[Depends(guarder)])


@user_router.get("/")
async def get_all_users():
    ...


@user_router.get("/{user_email}", response_model=UserAD)
async def get_more_info_user(*, user_email: str):
    ...


@user_router.post("/", response_model=UserAD)
async def create_new_user():
    ...


@user_router.post("/{user_email}", response_model=UserAD)
async def change_exist_user(*, user_email: str):
    ...


@user_router.delete("/{user_email}", response_model=UserAD)
async def delete_exist_user(*, user_email: str):
    ...


@user_router.post("/role/", include_in_schema=True)
async def create_new_role(role: RoleDB):
    ...


@user_router.post("/role/{role_name}", include_in_schema=True)
async def change_exist_role(*, role_name: str):
    ...
