import aiohttp
import json
from application.schemas.shop import shop
from application.schemas.PatternSchema import adapter

async def get_categories():
    async with aiohttp.ClientSession() as session:
        result = await session.get('http://future-backend.tw1.ru:8003/api/categories')
        print(await result.text())
        shop["categories"] = adapter.validate_python(await result.text())
        shop["categories_name"] = []
        for i in shop["categories"]:
            shop["categories_name"].append(i.name)