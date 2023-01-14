from datetime import datetime
from pydantic import BaseModel


class NewPost(BaseModel):
    date: datetime
    author: str
    text: str
    image: list[str]
