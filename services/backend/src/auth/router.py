from fastapi import APIRouter

from src.auth.schemas import AccessToken

auth_router = APIRouter(prefix="/auth")


@auth_router.post(path="/sign-in", status_code=200)
async def sing_in(token: AccessToken):
    ...


@auth_router.post(path="/sign-up", status_code=200)
async def sign_up():
    ...

