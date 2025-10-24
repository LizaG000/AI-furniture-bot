import aiohttp
import json
from application.schemas.users import users
from presentation.handlers.products.shema import adapter
from application.servers.buttons.buttons import product_message

async def get_products(id_chat: int, bot):
    async with aiohttp.ClientSession() as session:
        params={'categories': users[id_chat]["categories"],
                'colors': users[id_chat]["colors"],
                'materials': users[id_chat]["materials"]}
        result = await session.get('http://future-backend.tw1.ru:8003/api/products', params=params)
        products = adapter.validate_python(json.loads(await result.text()))
        users[id_chat]["products"] = products
        users[id_chat]["count"] = 1
        markup = product_message(id_chat, 0, products)
        users[id_chat]["index"] = 0
        with open(f"images/{products[0].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                id_chat,
                photo,
                caption=f"<b>{products[0].name}</b>\n{products[0].description}\n\nЦена: {products[0].price / 100 * (100-products[0].discount)}₽",
                parse_mode="HTML",
                reply_markup=markup
            )
        
        return products
