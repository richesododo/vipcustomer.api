from fastapi import APIRouter, HTTPException, Depends
from .schemas import SearchResponseSchema, SearchParamsSchema, SearchListSchema
from .services import SearchService
from typing import List
from db.db import db_session
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter()


@router.get("/", response_model=List[SearchResponseSchema])
async def search_vips(
    name: str,
    gender: str = None,
    occupation: str = None,
    age: int = None,
    email: str = None,
    session: AsyncSession = Depends(db_session)
):

    try:
        search_service = SearchService(session=session)
        resp = await search_service.search(
            {
                "name": name,
                "gender": gender,
                "occupation": occupation,
                "age": age,
                "email": email,
            }
        )

        return resp

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while validating VIP",
        )


@router.post("/search-many")
async def search_vip_list(params: SearchListSchema, session: AsyncSession = Depends(db_session)):
    try:
        data = [i.__dict__ for i in params.data]
        search_service = SearchService(session=session)
        resp = await search_service.search(data)
        return resp

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail="An error occurred while validating VIP",
        )
