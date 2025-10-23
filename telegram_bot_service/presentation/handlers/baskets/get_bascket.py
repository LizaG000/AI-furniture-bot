import aiohttp
from telebot.handler_backends import State, StatesGroup
from application.schemas.users import users
from application.servers.buttons.buttons import basket_message
from telebot import types
from application.servers.get_bascket import get_bascket

def basket_handlers(bot):

    @bot.message_handler(commands=['basket'])
    async def get_baskets(message):
        if message.chat.id not in users:
            users[message.chat.id] = {}
        users[message.chat.id]["basket"] = await get_bascket(message.chat.id)
        basket = users[message.chat.id]["basket"]
        if basket == []:
            await bot.send_message(message.chat.id, 'У вас пусто в корзине.')
        else:
            users[message.chat.id]["index_basket"] = 0
            print(users[message.chat.id])
            await bot.send_message(message.chat.id, 'Ваши товары')
            with open(f"images/{basket[0].images[0]}.png", "rb") as photo:
                await bot.send_photo(
                    message.chat.id,
                    photo,
                    caption=f"<b>{basket[0].name}</b>\n{basket[0].description}\n\nЦена: {basket[0].price / 100 * (100-basket[0].discount)}₽",
                    parse_mode="HTML",
                    reply_markup=basket_message(message.chat.id, 0)
                )
            
