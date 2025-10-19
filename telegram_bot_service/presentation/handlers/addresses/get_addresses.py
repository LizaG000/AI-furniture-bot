import aiohttp
from telebot.asyncio_storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from typing import List, Dict, Union
from application.schemas.AddressSchemas import AddressSchema
from application.servers.validation import validation_str_num

address: List[Dict[str, Union[int, AddressSchema]]] = []

def get_addresses_handlers(bot):
    class Address(StatesGroup):
        country = State()
        region = State()
        city = State()
        street = State()
        house_number = State()
        quadrature_number = State()
        postal_code = State()

    @bot.message_handler(commands=['list_addresses', 'список_адресов'])
    async def get_addresses(message):
        async with aiohttp.ClientSession() as session:
                params={'id_user': str(message.from_user.id)}
                print(params)
                result = await session.get('http://future-backend.tw1.ru:8003/api/address', params=params)
                print(await result.text())
        # await bot.send_message(message.chat.id, 'Введите страну.')
        # await bot.set_state(message.from_user.id, Address.country, message.chat.id)

