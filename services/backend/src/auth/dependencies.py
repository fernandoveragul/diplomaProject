from datetime import timedelta, datetime
from typing import Coroutine

from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src import config
from src.auth.schemas import TokenData
from src.config import SECRET_KEY, ALGO
from src.database import get_async_session
from src.users.models import user
from src.users.schemas import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class DPassword:
    """
    Depends password
    """
    CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def verify_pass(*, plain_pass, hashed_pass):
        DPassword.CONTEXT.verify(plain_pass, hashed_pass)

    @staticmethod
    async def do_hash(*, password: str):
        return DPassword.CONTEXT.hash(password)


class DToken:
    """
    Depends token
    """
    CREDENTIALS_EXCEPTION = credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/login/token")

    @staticmethod
    def create_token(*, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
        except JWTError:
            raise DToken.CREDENTIALS_EXCEPTION
        return encoded_jwt

    @staticmethod
    async def decode_jwt(*, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
            username: str = payload.get("sub")
            if username is None:
                raise DToken.CREDENTIALS_EXCEPTION
            token_data = TokenData(username=username)
        except JWTError:
            raise DToken.CREDENTIALS_EXCEPTION
        return token_data


class DAuth(DPassword, DToken):
    @staticmethod
    async def get_cur_user(*, username: str, session: AsyncSession = Depends(get_async_session)) -> User:
        usr = await session.execute(select(user).where(user.c.email_user == username))
        return User.from_orm(usr.first())

    @staticmethod
    async def authenticate_user(*, usr: User, password: str):
        if not usr:
            raise DAuth.CREDENTIALS_EXCEPTION
        if not DAuth.verify_pass(plain_pass=password, hashed_pass=usr.hashed_password_user):
            raise DAuth.CREDENTIALS_EXCEPTION
        return usr

    @staticmethod
    async def get_current_user_from_token(token: str = Depends(DToken.OAUTH2_SCHEME)):
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGO])
            username: str = payload.get("sub")
            if username is None:
                raise DToken.CREDENTIALS_EXCEPTION
        except JWTError:
            raise DToken.CREDENTIALS_EXCEPTION
        usr = DAuth.get_cur_user(username=username)
        if usr is None:
            raise DToken.CREDENTIALS_EXCEPTION
        return usr
