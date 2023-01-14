from fastapi import APIRouter

router = APIRouter(
    prefix="/student"
)


@router.get("/")
async def get_main_info_for_student():
    ...
