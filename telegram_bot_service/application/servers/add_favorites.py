import aiohttp
from uuid import UUID
import json
from application.schemas.shop import shop
from application.schemas.PatternSchema import adapter

async def add_favorites(id_user:int, id_product: UUID):
    async with aiohttp.ClientSession() as session:
        params={'id_user': id_user,
                'id_product': str(id_product)}
        result = await session.post('http://future-backend.tw1.ru:8003/api/favorites', json=params)
        return result.status