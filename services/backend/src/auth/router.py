from fastapi import APIRouter, status, Depends

from src.users.schemas import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post(path="/sign-in", status_code=status.HTTP_202_ACCEPTED)
async def sing_in():
    ...


@auth_router.post(path="/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up():
    ...


@auth_router.get("/me", status_code=status.HTTP_202_ACCEPTED)
async def read_users_me(current_user: User):
    ...
