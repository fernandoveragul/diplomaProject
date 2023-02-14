from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.auth.schemas import TokenData
from src.config import SECRET_KEY, ALGO

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

    @staticmethod
    async def create_token(*, data: dict, expires_delta: timedelta | None = None):

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
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
