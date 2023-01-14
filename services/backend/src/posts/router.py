from fastapi import APIRouter

router = APIRouter(
    prefix="post"
)


@router.get("/{post_id}", status_code=200)
async def get_post_by_id(post_id: int) -> dict:
    return {"POST": post_id}
