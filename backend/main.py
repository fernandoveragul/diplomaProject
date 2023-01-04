from fastapi import FastAPI
import uvicorn

application = FastAPI()


@application.get("/")
async def index():
    return {b'HELLO WORLD': 2022}


if __name__ == '__main__':
    uvicorn.run(app='main:application', host='0.0.0.0', port=49567, reload=True)
