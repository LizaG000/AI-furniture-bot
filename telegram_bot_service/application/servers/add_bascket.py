import aiohttp
from uuid import UUID
import json
from application.data.shop import shop
from application.schemas.PatternSchema import adapter

async def add_bascket(id_user:int, id_product: UUID, count:int):
    async with aiohttp.ClientSession() as session:
        params={'id_user': id_user,
                'id_product': str(id_product),
                'count': count}
        result = await session.post('http://future-backend.tw1.ru:8003/api/basckets', json=params)
        return result.status