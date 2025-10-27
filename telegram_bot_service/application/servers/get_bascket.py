import aiohttp
import json
from application.data.users import users
from presentation.handlers.baskets.schema import adapter
from application.servers.buttons.buttons import product_message

async def get_bascket(id_chat: int):
    async with aiohttp.ClientSession() as session:
        print(users[id_chat][id_chat].id)
        params={'data': users[id_chat][id_chat].id}
        print(params)
        result = await session.get('http://future-backend.tw1.ru:8003/api/basckets', params=params)
        print(await result.text())
        baskets = adapter.validate_python(json.loads(await result.text()))
        return baskets
