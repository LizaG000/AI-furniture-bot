import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter
from telebot.asyncio_storage import StateMemoryStorage

storage = StateMemoryStorage()
bot = AsyncTeleBot(token="8391809243:AAGi-OMZxGl3PnAuMeIW-xDi0UntJEes-vM",parse_mode="HTML", colorful_logs=True, state_storage=storage)


from presentation.handlers.registration_handlers import registration_handlers
from presentation.handlers.addresses.create_addresses import create_address_handlers
from presentation.handlers.addresses.get_addresses import get_addresses_handlers
from presentation.handlers.addresses.delete_address import delete_addresses_handlers
from application.servers.buttons.function import button_function
from application.servers.get_categories import get_categories
from application.servers.get_colors import get_colors
from application.servers.get_materials import get_materials
from presentation.handlers.products.get_products import get_products_handlers
from presentation.handlers.baskets.get_bascket import basket_handlers
from presentation.handlers.favorites.get_favorites import favorites_handlers
from application.schemas.users import users
from application.schemas.UserSchemas import CreateUser

bot.add_custom_filter(StateFilter(bot))


async def main():
    users[986213540]={}
    users[986213540][986213540] = CreateUser(
        id=986213540,
        first_name="Е",
        last_name="T",
        middle_name="f",
        phone=12,
        email="mmmm@mail.ru"
    )
    print(users)
    await get_categories()
    await get_colors()
    await get_materials()
    button_function(bot)
    registration_handlers(bot)
    create_address_handlers(bot)
    get_addresses_handlers(bot)
    delete_addresses_handlers(bot)
    get_products_handlers(bot)
    favorites_handlers(bot)
    basket_handlers(bot)
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())