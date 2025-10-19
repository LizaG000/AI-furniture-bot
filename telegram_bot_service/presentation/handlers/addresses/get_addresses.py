import aiohttp
import json
from application.servers.get_addresses import get_addresses_list



def get_addresses_handlers(bot):
    @bot.message_handler(commands=['list_addresses', 'список_адресов'])
    async def get_addresses(message):
        addresses = await get_addresses_list(message.from_user.id)
        await bot.send_message(message.chat.id, addresses)

