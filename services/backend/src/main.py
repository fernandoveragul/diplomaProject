from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.users.router import news_router as users_router
from src.auth.router import auth_router
from src.news.router import news_router

app = FastAPI()

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

app.include_router(users_router, tags=["user"])
app.include_router(news_router, tags=["routes"])
app.include_router(auth_router, tags=["authorization"])
