import aiohttp
import json
from uuid import UUID
from application.schemas.users import users
from presentation.handlers.baskets.schema import adapter

async def update_bascket(id_chat: int, id_basket: UUID, count: int = 1):
    async with aiohttp.ClientSession() as session:
        params={'id': str(id_basket),
                'count': count}
        await session.put('http://future-backend.tw1.ru:8003/api/basckets', params=params)
