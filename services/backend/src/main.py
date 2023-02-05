from fastapi import FastAPI

from src.about_college.router import router as about_router
from src.news.router import router as news_router

app = FastAPI()

app.include_router(about_router)
app.include_router(news_router)


@app.get("/")
async def index():
    return {"MESSAGE": "HELLO 2023"}
