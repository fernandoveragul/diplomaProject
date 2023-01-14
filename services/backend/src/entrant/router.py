from fastapi import APIRouter

router = APIRouter(
    prefix="/entrant"
)


@router.get("/")
async def get_main_info_for_entrant():
    ...
