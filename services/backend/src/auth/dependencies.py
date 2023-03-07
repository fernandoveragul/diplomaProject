from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status, Depends, Response
from jose import jwt, JWTError
from passlib.context import CryptContext

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row

from src.auth.schemas import STokenData
from src.config import SECRET_KEY, ALGO, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from src.database import get_async_session
from src.users.models import MUser


class DPassword:
    CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def verify_pass(self, *, plain_pass, hashed_pass):
        return self.CONTEXT.verify(plain_pass, hashed_pass)

    async def do_hash(self, *, password: str):
        return self.CONTEXT.hash(password)


class DToken:
    CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )

    HAVE_NOT_TOKEN_TYPE = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not found token type. Try later."
    )

    HAVE_NOT_COOKIE = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden. You are not administrator."
    )

    TIMEOUT_CONNECT = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Connection timed out."
    )

    @staticmethod
    async def get_current_user(*, user_email: str, session: AsyncSession = Depends(get_async_session)) -> Row | None:
        response = await session.execute(select(MUser).where(MUser.email_user == user_email))
        response_ = response.first()
        return response_

    @staticmethod
    async def delete_cookie_tokens(response: Response = Depends()):
        response.delete_cookie(key="access_token", httponly=True, secure=True)
        response.delete_cookie(key="refresh_token", httponly=True, secure=True)

    async def generate_token(self, *, data: dict, token_type: str) -> str:
        to_encode = data.copy()

        if token_type not in ["access", "refresh"]:
            raise self.HAVE_NOT_TOKEN_TYPE

        if await self.get_current_user(user_email=data.get("sub")) is None:
            raise self.CREDENTIALS_EXCEPTION

        match token_type:
            case "access":
                expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
                to_encode.update({"exp": expire})
            case "refresh":
                expire = datetime.utcnow() + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
                to_encode.update({"exp": expire})

        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
        return encoded_jwt

    async def decode_access_token(self, *, token: str) -> STokenData | None:
        token_data: STokenData | None = None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
            username: str = payload.get("sub")
            scopes: list[str] = payload.get("scopes")
            print(username, scopes)
            if username is None or scopes is None:
                raise self.CREDENTIALS_EXCEPTION
            if await self.get_current_user(user_email=username) is None:
                raise self.CREDENTIALS_EXCEPTION
            token_data = STokenData(username=username, scopes=scopes)
        except JWTError:
            await self.update_access_token()
        return token_data

    async def update_access_token(self, request: Request = Depends()) -> None:
        if r_token := request.cookies.get("refresh_token"):
            try:
                payload = jwt.decode(r_token, SECRET_KEY, algorithms=[ALGO])
                if datetime.utcfromtimestamp(payload.get('exp')) > datetime.utcnow():
                    await self.generate_token(data=payload, token_type="access")
                else:
                    raise self.TIMEOUT_CONNECT
            except JWTError:
                raise self.CREDENTIALS_EXCEPTION
        else:
            raise self.HAVE_NOT_COOKIE


class DTokenGuard(DToken):

    async def __call__(self, request: Request):
        if "access_token" not in request.cookies:
            raise self.HAVE_NOT_COOKIE
        return await self.decode_access_token(token=request.cookies.get("access_token"))
