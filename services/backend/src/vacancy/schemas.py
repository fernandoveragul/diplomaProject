from pydantic import BaseModel


class Vacancy(BaseModel):
    position: str
