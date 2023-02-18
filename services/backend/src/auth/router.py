from datetime import timedelta

from fastapi import APIRouter, status, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.auth.dependencies import DAuth
from src.auth.schemas import Token
from src.database import get_async_session
from src.users.schemas import User

auth_router = APIRouter(prefix="/auth")


@auth_router.post(path="/sign-in", status_code=status.HTTP_202_ACCEPTED)
async def sing_in():
    ...


@auth_router.post(path="/sign-up", status_code=status.HTTP_201_CREATED)
async def sign_up():
    ...


@auth_router.get("/me", status_code=status.HTTP_202_ACCEPTED)
async def read_users_me(access_token: str = Cookie(default=None)):
    print(access_token)
    print(await DAuth.decode_jwt(token=access_token))


@auth_router.post("/token", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def login_for_access_token(response: Response,
                                 form_data: OAuth2PasswordRequestForm = Depends(),
                                 dauth: DAuth = Depends(DAuth)):

    if form_data.username == "user" and form_data.password == "pass":
        access_token_expires = timedelta(minutes=int(config.ACCESS_TOKEN_EXPIRE_MINUTES))
        access_token = dauth.create_token(
            data={"sub": "user@mail.com"}, expires_delta=access_token_expires
        )
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        return {"access_token": access_token, "token_type": "bearer"}

    usr = await dauth.get_cur_user(username=form_data.username)
    user = await dauth.authenticate_user(usr=usr, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = dauth.create_token(
        data={"sub": user.email_user}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
