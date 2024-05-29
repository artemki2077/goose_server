from fastapi import APIRouter, Depends

from depends import get_dataBaseService
from schemas.search_filter import SearchFilter
from services.database_service import DataBaseService
from fuzzywuzzy import fuzz

router = APIRouter(prefix="/data", tags=['data'])


@router.post("/search")
async def get_search(
    search_filter: SearchFilter | None = None,
    search: str | None = None,
    db: DataBaseService = Depends(get_dataBaseService)
):
    if search_filter is None:
        search_filter = SearchFilter()

    data_from_db = await db.get_all()
    if data_from_db is None:
        data_from_db = []

    data_from_db = list(filter(lambda x: search_filter.price_min < x.price < search_filter.price_max, data_from_db))

    if search:
        data_from_db.sort(key=lambda x: fuzz.partial_ratio(search, x.name), reverse=True)
        return data_from_db
    return list(map(lambda x: x.model_dump(mode="json"), data_from_db))


@router.get("/product")
async def get_product():
    ...