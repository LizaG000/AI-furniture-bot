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
from application.schemas.shop import shop

bot.add_custom_filter(StateFilter(bot))


async def main():
    await get_categories()
    await get_colors()
    await get_materials()
    print(shop)
    button_function(bot)
    registration_handlers(bot)
    create_address_handlers(bot)
    get_addresses_handlers(bot)
    delete_addresses_handlers(bot)
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())