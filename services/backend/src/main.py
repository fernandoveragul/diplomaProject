from fastapi import FastAPI
import uvicorn

application = FastAPI(
    title='College new site'
)


@application.get("/")
async def index():
    return {b'HELLO WORLD': 2022}


@application.get("/hello")
async def hello():
    return b"HELLO"
