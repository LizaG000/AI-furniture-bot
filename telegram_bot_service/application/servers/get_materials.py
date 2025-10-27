import aiohttp
import json
from application.data.shop import shop
from application.schemas.PatternSchema import adapter

async def get_materials():
    async with aiohttp.ClientSession() as session:
        result = await session.get('http://future-backend.tw1.ru:8003/api/materials')
        shop["materials"] = adapter.validate_python(json.loads(await result.text()))
        shop["materials_name"] = []
        for i in shop["materials"]:
            shop["materials_name"].append(i.name)