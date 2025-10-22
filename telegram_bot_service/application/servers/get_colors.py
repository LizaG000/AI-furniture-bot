import aiohttp
import json
from application.schemas.shop import shop
from application.schemas.PatternSchema import adapter

async def get_colors():
    async with aiohttp.ClientSession() as session:
        result = await session.get('http://future-backend.tw1.ru:8003/api/colors')
        shop["colors"] = adapter.validate_python(json.loads(await result.text()))
        shop["colors_name"] = []
        for i in shop["colors"]:
            shop["colors_name"].append(i.name)