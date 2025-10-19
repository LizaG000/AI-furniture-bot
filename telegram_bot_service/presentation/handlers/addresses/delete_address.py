import aiohttp
import json
from telebot.handler_backends import State, StatesGroup
from application.servers.get_addresses import get_addresses_list
from application.schemas.AddressSchemas import AddressSchema

list_addresses = str
addresses = list[str]
results = list[AddressSchema]

def delete_addresses_handlers(bot):

    
    class Address(StatesGroup):
        delete_address = State()

    @bot.message_handler(commands=['delete_address', 'удалить_адрес'])
    async def delete_address_number(message):
        list_addresses, addresses, results = await get_addresses_list(message.from_user.id)
        answer = "Введите номер адреса, который хотите удалить:\n" + list_addresses
        await bot.send_message(message.chat.id, answer)
        await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
    

    @bot.message_handler(state=Address.delete_address)
    async def delete_address_number(message):
        answer = message.text
        if answer not in [str(i+1) for i in range(len(addresses))]:
            await bot.send_message(message.chat.id, "Упс, вы куда-то не туда нажали. Пожалуйста введите номер адреса из списка:\n" + list_addresses)
            await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
        async with aiohttp.ClientSession() as session:
            params={'id_user': str(addresses[int(answer)].id)}
            result = await session.get('http://future-backend.tw1.ru:8003/api/address', params=params)
            print(result)
            print(result.status)
            await bot.send_message(message.chat.id, await result.text())




