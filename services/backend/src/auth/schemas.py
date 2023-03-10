from pydantic import BaseModel, Field


class SToken(BaseModel):
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field(..., alias="tokenType")


class STokenData(BaseModel):
    username: str | None = Field(None, alias="username")
    scope: list[str] | None = Field(None, alias="scope")
