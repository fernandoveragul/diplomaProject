from fastapi import Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer
from passlib.context import CryptContext

from src.users.schemas import User

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
    async def create_token(cls, *, data: dict):
        ...


def fake_decode_token(token):
    return User(
        nickname_user=token + "fakedecoded", email_user="john@example.com")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    return user
