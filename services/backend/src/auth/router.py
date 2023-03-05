from datetime import timedelta

from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.dependencies import DTokenGuard
from src.config import ACCESS_TOKEN_EXPIRE_MINUTES

guarder = DTokenGuard()
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/sign-up")
async def sign_up():
    ...


@auth_router.post("/sign-in")
def sign_in(response: Response,
            form_data: OAuth2PasswordRequestForm = Depends(),
            guard: DTokenGuard = Depends(DTokenGuard)):
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = guard.generate_access_token(data={
        "sub": form_data.username,
        "scopes": form_data.scopes
    }, expires_delta=access_token_expires)

    response.set_cookie(key="access_token", value=access_token,
                        httponly=True, secure=True)


@auth_router.post("/logout")
async def logout():
    ...
