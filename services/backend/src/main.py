from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users.router import user_router
from src.auth.router import auth_router
from src.news.router import news_router

import uvicorn

app = FastAPI(title="API")

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"]
)


@app.get("/")
async def index():
    return "hello"


app.include_router(user_router, tags=["users"])
app.include_router(news_router, tags=["news"])
app.include_router(auth_router, tags=["auth"])

if __name__ == '__main__':
    uvicorn.run("src.main:app", reload=True)