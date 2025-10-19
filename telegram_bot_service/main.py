import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter

bot = AsyncTeleBot("8391809243:AAGi-OMZxGl3PnAuMeIW-xDi0UntJEes-vM")

from presentation.handlers.registration_handlers import registration_handlers
from presentation.handlers.addresses.create_addresses import create_address_handlers
from presentation.handlers.addresses.get_addresses import get_addresses_handlers
from presentation.handlers.addresses.delete_address import delete_addresses_handlers

bot.add_custom_filter(StateFilter(bot))

async def main():
    registration_handlers(bot)
    create_address_handlers(bot)
    get_addresses_handlers(bot)
    delete_addresses_handlers(bot)
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())