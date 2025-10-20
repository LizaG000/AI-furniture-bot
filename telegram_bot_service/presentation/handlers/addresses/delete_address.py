import aiohttp
import json

from sqlalchemy.testing.suite.test_reflection import users
from telebot.handler_backends import State, StatesGroup
from application.servers.get_addresses import get_addresses_list
from application.schemas.AddressSchemas import AddressSchema

def delete_addresses_handlers(bot):
    users_addresses = {}
    class Address(StatesGroup):
        delete_address = State()

    @bot.message_handler(commands=['delete_address', 'удалить_адрес'])
    async def delete_address_number(message):
        print(1)
        text, addresses, results = await get_addresses_list(message.from_user.id)
        users_addresses[message.from_user.id] = {
            "text": text,
            "addresses": addresses,
            "results":results
        }
        print(2)
        answer = "Введите номер адреса, который хотите удалить:\n" + text
        print(2)
        await bot.send_message(message.chat.id, answer)
        print(2)
        await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
    

    @bot.message_handler(state=Address.delete_address)
    async def delete_address_number(message):
        text = users_addresses[message.from_user.id]["text"]
        addresses = users_addresses[message.from_user.id]["addresses"]
        results = users_addresses[message.from_user.id]["results"]
        answer = message.text
        if answer not in [str(i+1) for i in range(len(text))]:
            await bot.send_message(message.chat.id, "Упс, вы куда-то не туда нажали. Пожалуйста введите номер адреса из списка:\n" + text)
            await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
        async with aiohttp.ClientSession() as session:
            params={'id': str(results[int(answer)-1].id)}
            result = await session.delete('http://future-backend.tw1.ru:8003/api/address', params=params)
            print(result)
            print(result.status)
            await bot.send_message(message.chat.id, await result.text())




