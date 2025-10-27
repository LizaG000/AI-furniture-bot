import aiohttp
import json
from application.data.shop import shop
from application.schemas.PatternSchema import adapter

async def get_categories():
    async with aiohttp.ClientSession() as session:
        result = await session.get('http://future-backend.tw1.ru:8003/api/categories')
        shop["categories"] = adapter.validate_python(json.loads(await result.text()))
        shop["categories_name"] = []
        for i in shop["categories"]:
            shop["categories_name"].append(i.name)