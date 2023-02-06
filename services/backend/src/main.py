from fastapi import FastAPI

from src.users.router import router as users_router
from src.news.router import router as news_router

app = FastAPI()

app.include_router(users_router)
app.include_router(news_router)


@app.get("/")
async def index():
    return {"MESSAGE": "HELLO 2023"}
