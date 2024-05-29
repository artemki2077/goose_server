from pydantic_redis.asyncio import Model
import datetime as dt


class Product(Model):
    _primary_key_field = "original_link"
    last_update: dt.datetime
    name: str
    price: int  # руб
    img_url: str | None = None
    original_link: str
    add_data: dict = {}


