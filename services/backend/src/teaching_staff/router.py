from fastapi import APIRouter

router = APIRouter(
    prefix="/teaching-staff"
)


@router.get("/")
async def get_main_info_teaching_staff():
    ...
