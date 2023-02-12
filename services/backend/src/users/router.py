from fastapi import APIRouter

router = APIRouter(prefix="/about")


@router.get("/")
async def get_main_info_about_college(type_about=None):
    ...
