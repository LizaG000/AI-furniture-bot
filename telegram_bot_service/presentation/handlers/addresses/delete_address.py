import aiohttp
import json
from telebot import types
from application.data.users import users
from telebot.handler_backends import State, StatesGroup
from application.servers.get_addresses import get_addresses_list
from application.servers.buttons.buttons import return_button
from application.data.states import Address

def delete_addresses_handlers(bot):

    @bot.message_handler(commands=['delete_address', 'удалить_адрес'])
    async def delete_address_number(message):
        if message.chat.id not in users:
            users[message.chat.id] = {}
        if message.chat.id not in users[message.from_user.id]:
            await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
        else:
            if "text" not in users[message.chat.id] or users[message.chat.id]["text"] == "":
                await get_addresses_list(message.from_user.id, message.chat.id)
            if users[message.chat.id]["text"] == "":
                await bot.send_message(message.chat.id, "Упс. Кажется у вас еще нет адресов(")
            else:
                answer = "Введите номер адреса, который хотите удалить:\n" + users[message.chat.id]["text"]
                await bot.send_message(message.chat.id, answer, reply_markup=return_button())
                await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
    

    @bot.message_handler(state=Address.delete_address)
    async def delete_address_number(message):
        text = users[message.from_user.id]["text"]
        addresses = users[message.from_user.id]["addresses"]
        results = users[message.from_user.id]["results"]
        answer = message.text
        if answer not in [str(i+1) for i in range(len(text))]:
            await bot.send_message(message.chat.id, "Упс, вы куда-то не туда нажали. Пожалуйста введите номер адреса из списка:\n" + text)
            await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
        async with aiohttp.ClientSession() as session:
            params={'id': str(results[int(answer)-1].id)}
            await session.delete('http://future-backend.tw1.ru:8003/api/address', params=params)
            await bot.send_message(message.chat.id, "Успешно удален адрес: \n"+addresses[int(answer)-1], reply_markup=types.ReplyKeyboardRemove())
            await get_addresses_list(message.from_user.id, message.chat.id)
            await bot.set_state(message.from_user.id, None, message.chat.id)




