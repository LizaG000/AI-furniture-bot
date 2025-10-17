import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_filters import StateFilter

bot = AsyncTeleBot("8391809243:AAGi-OMZxGl3PnAuMeIW-xDi0UntJEes-vM")

from registration_handlers import registration_handlers

bot.add_custom_filter(StateFilter(bot))

async def main():
    registration_handlers(bot)
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())