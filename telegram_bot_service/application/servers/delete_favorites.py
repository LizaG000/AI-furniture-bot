import aiohttp
import json
from uuid import UUID
from application.schemas.users import users
from application.servers.get_favorites import get_favorites

async def delete_favorites(id_chat: int, id_favorites: UUID):
    async with aiohttp.ClientSession() as session:
        params={'id': str(id_favorites)}
        result = await session.delete('http://future-backend.tw1.ru:8003/api/favoritess', params=params)
        users[id_chat]["favorites"] = await get_favorites(id_chat)
        return result.status
