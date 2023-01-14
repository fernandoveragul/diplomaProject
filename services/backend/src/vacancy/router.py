from fastapi import APIRouter

router = APIRouter(
    prefix="/vacancy"
)


@router.get("/")
async def get_all_vacancy():
    ...
