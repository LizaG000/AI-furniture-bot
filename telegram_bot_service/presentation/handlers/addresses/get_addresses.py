from application.servers.get_addresses import get_addresses_list
from application.schemas.users import users



def get_addresses_handlers(bot):
    @bot.message_handler(commands=['list_addresses', 'список_адресов'])
    async def get_addresses(message):
        if message.chat.id not in users:
            await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
        else:
            if "text" not in users[message.chat.id]:
                await get_addresses_list(message.from_user.id)
            await bot.send_message(message.chat.id, users[message.chat.id]["text"])

