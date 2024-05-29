from pydantic import BaseModel


class SearchFilter(BaseModel):
    price_max: int | float = 9999999999999
    price_min: int | float = 0
