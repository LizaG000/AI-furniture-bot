import aiohttp
import json
from uuid import UUID
from application.schemas.users import users
from application.servers.get_bascket import get_bascket

async def delete_bascket(id_chat: int, id_basket: UUID):
    async with aiohttp.ClientSession() as session:
        params={'id': str(id_basket)}
        print(params)
        result = await session.delete('http://future-backend.tw1.ru:8003/api/basckets', params=params)
        print(await result.text())
        return result.status
