from fastapi import APIRouter, status, Depends

from src.auth.dependencies import get_current_user
from src.auth.schemas import AccessToken
from src.users.schemas import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post(path="/sign-in", status_code=status.HTTP_202_ACCEPTED)
async def sing_in(token: AccessToken):
    ...


@auth_router.post(path="/sign-up", status_code=200)
async def sign_up():
    ...


@auth_router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
