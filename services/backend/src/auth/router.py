from fastapi import APIRouter, Depends, Response, status, HTTPException, Body
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import DTokenGuard, DPassword
from src.auth.schemas import Token
from src.database import get_async_session
from src.users.models import Users
from src.users.schemas import UserDB, UserAD
from src.users.schemas import User

guarder = DTokenGuard()
auth_router = APIRouter(prefix="/auth")


@auth_router.post("/sign-up", status_code=status.HTTP_201_CREATED, response_model=User)
async def sign_up(user_data: UserAD,
                  password: str = Body(...),
                  passer: DPassword = Depends(),
                  session: AsyncSession = Depends(get_async_session)):

    usr = UserDB(email_user=user_data.email_user,
                 hashed_password=await passer.do_hash(password=password),
                 personal_data=user_data.personal_data,
                 role_user=user_data.role_user)
    try:
        await session.execute(insert(Users).values(**usr.dict()))
        return usr
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Incorrect user data\n{user_data.dict()}")


@auth_router.post("/sign-in", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
async def sign_in(response: Response, form_data: OAuth2PasswordRequestForm = Depends(),
                  guard: DTokenGuard = Depends(), passer: DPassword = Depends()):
    if form_data.grant_type not in ["access", "refresh"]:
        raise guard.HAVE_NOT_TOKEN_TYPE

    if usr_dt := await guard.get_current_user(user_email=form_data.username) is None:
        raise guard.CREDENTIALS_EXCEPTION
    else:
        usr: UserDB = UserDB(**usr_dt)
        if not await passer.verify_pass(plain_pass=form_data.password, hashed_pass=usr.hashed_password):
            raise guard.CREDENTIALS_EXCEPTION
        else:
            access_token = await guard.generate_token(data={
                "sub": form_data.username,
                "scopes": form_data.scopes
            }, token_type="assess")

            refresh_token = await guard.generate_token(data={
                "sub": form_data.username,
                "scopes": form_data.scopes
            }, token_type="refresh")

            response.set_cookie(key="access_token", value=access_token,
                                httponly=True, secure=True)
            response.set_cookie(key="refresh_token", value=refresh_token,
                                httponly=True, secure=True)
            return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout", status_code=status.HTTP_200_OK, response_model=User)
async def logout():
    ...
