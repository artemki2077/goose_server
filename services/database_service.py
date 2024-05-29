from pydantic_redis.asyncio import Store, RedisConfig
from schemas.product import Product


class DataBaseService:
    def __init__(self,
                 host: str = "localhost",
                 password: str | None = None,
                 port: int = 6379,
                 ):
        """
        :param host: хост это домен или ip адрес сервера, где находиться redis сервер
        :param password: пароль от redis сервера, по дефолту и без настройки редис сервера его можно не указывать
        :param port: порт на сервере на котором работает redis по дефолту он 6379
        """
        self.product_store = Store(
            name="product_store",
            redis_config=RedisConfig(
                host=host,
                password=password,
                port=port
            )
        )
        self.product = Product
        self.product_store.register_model(self.product)

    async def get_all(self) -> Product | list[Product]:
        return await self.product.select()

    async def get_by_id(self, _id=0):
        return await self.product.select(skip=_id, limit=1)

    async def add_product(self, data: Product | list[Product]):
        await self.product.insert(data)

