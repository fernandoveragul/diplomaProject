from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from src.auth.schemas import TokenData
from src.config import SECRET_KEY, ALGO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TVPassword:
    """
    Token, Veryfi, Password and another
    """
    CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    async def verify_pass(cls, *, plain_pass, hashed_pass):
        TVPassword.CONTEXT.verify(plain_pass, hashed_pass)

    @classmethod
    async def do_hash(cls, *, password: str):
        return TVPassword.CONTEXT.hash(password)

    @classmethod
    async def create_token(cls, *, data: dict, expires_delta: timedelta | None = None):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        try:
            encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
        except JWTError:
            raise credentials_exception
        return encoded_jwt

    @classmethod
    async def decode_jwt(cls, *, token):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        return token_data
