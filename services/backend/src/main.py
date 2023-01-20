from fastapi import FastAPI

from src.about_college.router import router as about_router
from src.entrant.router import router as entrant_router
from src.news.router import router as news_router
from src.student.router import router as student_router
from src.teaching_staff.router import router as teaching_router
from src.vacancy.router import router as vacancy_router

app = FastAPI()

app.include_router(about_router)
app.include_router(entrant_router)
app.include_router(news_router)
app.include_router(student_router)
app.include_router(teaching_router)
app.include_router(vacancy_router)


@app.get("/")
async def index():
    return {"MESSAGE": "HELLO 2023"}
