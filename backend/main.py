from fastapi import FastAPI
import uvicorn

application = FastAPI()


@application.get("/")
async def index():
    return {b'HELLO WORLD': 2022}


def run():
    uvicorn.run(app='main:application', host='localhost', port=48569, reload=True)


if __name__ == '__main__':
    run()
