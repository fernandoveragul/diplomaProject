from fastapi import FastAPI
from src.news.router import router as post_router
from src.about_college.router import router as about_router


app = FastAPI()

app.include_router(post_router)
app.include_router(about_router)


@app.get("/")
async def index():
    return {"MESSAGE": "HELLO 2023"}
