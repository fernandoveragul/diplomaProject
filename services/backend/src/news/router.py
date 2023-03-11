import json

from fastapi import APIRouter, status, Depends, HTTPException, Body
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.auth.dependencies import DTokenGuard
from src.database import get_async_session
from src.news.schemas import SNews, SNewsDB, SNewsAD
from src.news.models import MNews

news_router = APIRouter(prefix="/nws")
guarder = DTokenGuard()


@news_router.get("/",
                 status_code=status.HTTP_200_OK,
                 response_model=list[SNews],
                 summary="Endpoint return list all news posts")
async def get_all_news_posts(session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews))
    if response.scalars().first():
        result: list[SNewsDB] = [SNewsDB.from_orm(news_post) for news_post in response.scalars().all()]
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid request")


@news_router.get("/single",
                 status_code=status.HTTP_200_OK,
                 response_model=SNewsAD,
                 summary="Endpoint return single news post")
async def get_single_news_post(news_post_single: SNews = Body(..., alias="newsPostSingle"),
                               session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews).where(MNews.author_news == news_post_single.author_news and
                                                         MNews.header_news == news_post_single.header_news and
                                                         MNews.text_news == news_post_single.text_news and
                                                         MNews.specific == news_post_single.specific))
    if res := response.scalars().first():
        result = SNewsDB.from_orm(res)
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid request data\n"
                                   f"data: {json.dumps(news_post_single.dict(), indent=4)}")


@news_router.post("/create", status_code=status.HTTP_201_CREATED,
                  response_model=SNewsAD,
                  dependencies=[Depends(guarder)],
                  summary="Endpoint create new news post")
async def create_new_news_post(news_post_create: SNews = Body(..., alias="newsPostCreate"),
                               session: AsyncSession = Depends(get_async_session)):
    invalid_take_data = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                      detail=f"Invalid request data\n"
                                             f"data: {json.dumps(news_post_create.dict(), indent=4)}")

    try:
        values: SNewsDB = SNewsDB(**news_post_create.dict())
        await session.execute(insert(MNews).values(**values.dict()))
        await session.commit()
        return values
    except SQLAlchemyError:
        raise invalid_take_data


@news_router.post("/update", status_code=status.HTTP_202_ACCEPTED,
                  response_model=SNewsAD,
                  dependencies=[Depends(guarder)],
                  summary="Endpoint change exist news post")
async def change_exist_news_post(news_post_exist: SNews = Body(..., alias="newsPostExist"),
                                 news_post_new: SNews = Body(..., alias="newsPostNew"),
                                 session: AsyncSession = Depends(get_async_session)):
    invalid_take_data = HTTPException(status_code=status.HTTP_409_CONFLICT,
                                      detail=f"Invalid request data\n"
                                             f"data: {json.dumps(news_post_new.dict(), indent=4)}")

    response = await session.execute(select(MNews).where(MNews.author_news == news_post_exist.author_news and
                                                         MNews.header_news == news_post_exist.header_news and
                                                         MNews.text_news == news_post_exist.text_news and
                                                         MNews.specific == news_post_exist.specific))
    if res := response.scalars().first():
        try:
            data = SNewsDB.from_orm(res)
            data.__dict__.update(news_post_new.dict())
            await session.execute(update(MNews).values(**data.dict()))
            await session.commit()
            return data
        except SQLAlchemyError:
            raise invalid_take_data
    else:
        raise invalid_take_data


@news_router.delete("/delete",
                    status_code=status.HTTP_202_ACCEPTED,
                    response_model=SNewsAD,
                    dependencies=[Depends(guarder)],
                    summary="Endpoint delete exist news post")
async def delete_exist_news_post(post_data_delete: SNewsAD = Body(..., alias="newsPostDelete"),
                                 session: AsyncSession = Depends(get_async_session)):
    response = await session.execute(select(MNews).where(MNews.uuid_news == post_data_delete.uuid_news))
    if response.scalars().first():
        await session.execute(delete(MNews).where(MNews.uuid_news == post_data_delete.uuid_news))
        await session.commit()
        return post_data_delete
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Invalid request data\ndata: {json.dumps(post_data_delete.dict(), indent=4)}")
