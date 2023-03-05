from datetime import datetime, timedelta

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Row

from src.auth.schemas import TokenData
from src.config import SECRET_KEY, ALGO, ACCESS_TOKEN_EXPIRE_MINUTES
from src.database import get_async_session
from src.users.models import User


class DToken:
    CREDENTIALS_EXCEPTION = credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    @staticmethod
    async def _get_current_user(*, user_email: str, session: AsyncSession = Depends(get_async_session)) -> Row | None:
        response = await session.execute(select(User).where(User.email_user == user_email))
        response_ = response.first()
        return response_

    def generate_access_token(self, *, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
        return encoded_jwt

    def decode_access_token(self, *, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
            username: str = payload.get("sub")
            scopes: list[str] = payload.get("scopes")
            print(username, scopes)
            if username is None:
                raise self.CREDENTIALS_EXCEPTION
            token_data = TokenData(username=username, scopes=scopes)
        except JWTError:
            raise self.CREDENTIALS_EXCEPTION
        return token_data

    def update_access_token(self):
        ...


class DTokenGuard(DToken):
    EXCEPTION_HAVE_NOT_COOKIE = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access forbidden. You are not administrator"
    )

    def __call__(self, request: Request):
        if "access_token" not in request.cookies:
            raise self.EXCEPTION_HAVE_NOT_COOKIE
        return self.decode_access_token(token=request.cookies.get("access_token"))
