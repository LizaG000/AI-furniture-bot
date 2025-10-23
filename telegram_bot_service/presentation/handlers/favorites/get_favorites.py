import aiohttp
from telebot.handler_backends import State, StatesGroup
from application.schemas.users import users
from application.servers.buttons.buttons import favorites_message
from telebot import types
from application.servers.get_favorites import get_favorites

def favorites_handlers(bot):

    @bot.message_handler(commands=['favorites'])
    async def get_favorite(message):
        if message.chat.id not in users:
            users[message.chat.id] = {}
        users[message.chat.id]["favorites"] = await get_favorites(message.chat.id)
        favorites = users[message.chat.id]["favorites"]
        favorites = users[message.chat.id]["favorites_index"] = 0
        await bot.send_message(message.chat.id, 'Ваши товары')
        with open(f"images/{favorites[0].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                message.chat.id,
                photo,
                caption=f"<b>{favorites[0].name}</b>\n{favorites[0].description}\n\nЦена: {favorites[0].price / 100 * (100-favorites[0].discount)}₽",
                parse_mode="HTML",
                reply_markup=favorites_message(message.chat.id, 0)
            )

            
