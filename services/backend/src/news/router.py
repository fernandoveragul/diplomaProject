import json

from fastapi import APIRouter, status, Depends, HTTPException, Body
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import DTokenGuard
from src.database import get_async_session
from src.news.schemas import SNews, SNewsPostData, SNewsDB
from src.news.models import MNews

news_router = APIRouter(prefix="/nws")
guarder = DTokenGuard()


@news_router.get("/",
                 status_code=status.HTTP_200_OK,
                 response_model=list[SNews],
                 summary="Endpoint return list all news posts")
async def get_all_news_posts(session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews))
    if response.first():
        result: list[SNewsDB] = [SNewsDB(news_post) for news_post in response.fetchall()]
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid request")


@news_router.get("/single",
                 status_code=status.HTTP_200_OK,
                 response_model=SNews,
                 summary="Endpoint return single news post")
async def get_single_news_post(post_data_single: SNewsPostData = Body(..., alias="postDataSingle"),
                               session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews).where(MNews.uuid_news == post_data_single.uuid_news))
    if res := response.first():
        result = SNewsDB(res)
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid request data\ndata: {json.dumps(post_data_single.dict(), indent=4)}")


@news_router.post("/", status_code=status.HTTP_201_CREATED,
                  response_model=SNews,
                  dependencies=[Depends(guarder)],
                  summary="Endpoint create new news post")
async def create_new_news_post(news_post: SNews = Body(..., alias="newsPost"),
                               session: AsyncSession = Depends(get_async_session)):
    invalid_take_data = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                      detail=f"Invalid request data\ndata: {json.dumps(news_post.dict(), indent=4)}")

    try:
        values: SNewsDB = SNewsDB(**news_post.dict())
        await session.execute(insert(MNews).values(**values.dict()))
        await session.commit()
        return news_post
    except SQLAlchemyError:
        raise invalid_take_data


@news_router.post("/update", status_code=status.HTTP_202_ACCEPTED,
                  response_model=SNews,
                  dependencies=[Depends(guarder)],
                  summary="Endpoint change exist news post")
async def change_exist_news_post(post_data_update: SNewsPostData = Body(..., alias="postDataUpdate"),
                                 news_post: SNews = Body(..., alias="newsPost"),
                                 session: AsyncSession = Depends(get_async_session)):
    invalid_take_data = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                      detail=f"Invalid request data\ndata: {json.dumps(news_post.dict(), indent=4)}")

    response = await session.execute(select(MNews).where(MNews.uuid_news == post_data_update))
    if response.first():
        try:
            await session.execute(update(MNews).values(**news_post.dict()))
            await session.commit()
            return news_post
        except SQLAlchemyError:
            raise invalid_take_data


@news_router.delete("/delete",
                    status_code=status.HTTP_202_ACCEPTED,
                    response_model=SNewsPostData,
                    dependencies=[Depends(guarder)],
                    summary="Endpoint delete exist news post")
async def delete_exist_news_post(post_data_delete: SNewsPostData = Body(..., alias="postDataDelete"),
                                 session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews).where(MNews.uuid_news == post_data_delete.uuid_news))
    if response.first():
        await session.execute(delete(MNews).where(MNews.uuid_news == post_data_delete.uuid_news))
        await session.commit()
        return post_data_delete
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(post_data_delete.dict(), indent=4)}")
