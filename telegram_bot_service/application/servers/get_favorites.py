import aiohttp
import json
from application.schemas.users import users
from presentation.handlers.favorites.schema import adapter
from application.servers.buttons.buttons import product_message

async def get_favorites(id_chat: int):
    async with aiohttp.ClientSession() as session:
        params={'id_user': users[id_chat][id_chat].id}
        result = await session.get('http://future-backend.tw1.ru:8003/api/favorites', params=params)
        favorites = adapter.validate_python(json.loads(await result.text()))
        return favorites
