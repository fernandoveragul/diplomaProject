from fastapi import APIRouter
from .schemas import TypeAboutInfo

router = APIRouter(prefix="/about")


@router.get("/")
async def get_main_info_about_college(type_about: TypeAboutInfo = None):
    ...
