import aiohttp
from telebot.asyncio_storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from application.schemas.AddressSchemas import CreateAddressSchema
from application.servers.validation import validation_str_num

address = CreateAddressSchema()

def create_address_handlers(bot):
    class Address(StatesGroup):
        country = State()
        region = State()
        city = State()
        street = State()
        house_number = State()
        quadrature_number = State()
        postal_code = State()

    @bot.message_handler(commands=['add_address', 'добавить_адрес'])
    async def add_address(message):
        await bot.send_message(message.chat.id, 'Введите страну.')
        await bot.set_state(message.from_user.id, Address.country, message.chat.id)

    @bot.message_handler(state=Address.country)
    async def address_country(message):
        country = message.text
        country = country.lower()
        country = validation_str_num(country)
        if not country:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста страну.')
            await bot.set_state(message.from_user.id, Address.country, message.chat.id)
        else:
            address.id_user = message.from_user.id
            address.country = country[0].upper() + country[1:]
            await bot.send_message(message.chat.id, 'Введите регион.')
            await bot.set_state(message.from_user.id, Address.region, message.chat.id)

    @bot.message_handler(state=Address.region)
    async def address_region(message):
        region = message.text
        region = region.lower()
        region = validation_str_num(region)
        if not region:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите регион.')
            await bot.set_state(message.from_user.id, Address.region, message.chat.id)
        else:
            address.region = region[0].upper() + region[1:]
            await bot.send_message(message.chat.id, 'Введите город.')
            await bot.set_state(message.from_user.id, Address.city, message.chat.id)

    @bot.message_handler(state=Address.city)
    async def address_city(message):
        city = message.text
        city = city.lower()
        city = validation_str_num(city)
        if not city:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите город.')
            await bot.set_state(message.from_user.id, Address.region, message.chat.id)
        else:
            address.city = city[0].upper() + city[1:]
            await bot.send_message(message.chat.id, 'Введите улицу.')
            await bot.set_state(message.from_user.id, Address.street, message.chat.id)

    @bot.message_handler(state=Address.street)
    async def address_street(message):
        street = message.text
        street = street.lower()
        street = validation_str_num(street)
        if not street:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите улицу.')
            await bot.set_state(message.from_user.id, Address.street, message.chat.id)
        else:
            address.id_user = message.from_user.id
            address.street = street[0].upper() + street[1:]
            await bot.send_message(message.chat.id, 'Введите номер дома.')
            await bot.set_state(message.from_user.id, Address.house_number, message.chat.id)

    @bot.message_handler(state=Address.house_number)
    async def address_house_number(message):
        house_number = message.text
        house_number = house_number.lower()
        house_number = validation_str_num(house_number)
        if not house_number:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите улицу.')
            await bot.set_state(message.from_user.id, Address.street, message.chat.id)
        else:
            address.house_number = house_number[0].upper() + house_number[1:]
            await bot.send_message(message.chat.id, 'Введите номер квартиры.')
            await bot.set_state(message.from_user.id, Address.quadrature_number, message.chat.id)

    @bot.message_handler(state=Address.quadrature_number)
    async def address_quadrature_number(message):
        quadrature_number = message.text
        quadrature_number = quadrature_number.lower()
        quadrature_number = validation_str_num(quadrature_number)
        if not quadrature_number:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите номер квартиры.')
            await bot.set_state(message.from_user.id, Address.quadrature_number, message.chat.id)
        else:
            address.quadrature_number = quadrature_number[0].upper() + quadrature_number[1:]
            await bot.send_message(message.chat.id, 'Введите почтовый код.')
            await bot.set_state(message.from_user.id, Address.postal_code, message.chat.id)
            

    @bot.message_handler(state=Address.postal_code)
    async def address_postal_code(message):
        try:
            postal_code = int(message.text)
            address.postal_code = postal_code
            try:
                async with aiohttp.ClientSession() as session:
                    data = address.__dict__
                    result = await session.post('http://future-backend.tw1.ru:8003/api/address', json=data)
                    if result.status == 200:
                        await bot.send_message(message.chat.id, f'Адрес Успешно добавден!\nСтрана: {address.country}\nРайон: {address.region}\nГород: {address.city}\nУлица: {address.street}\nНомер дома: {address.house_number}\nНомер квартиры: {address.quadrature_number}\nПочтовый код: {address.postal_code}')
                    else:
                        await bot.send_message(message.chat.id, f'Упс, не удалось установить соединение')
            except:
                await bot.send_message(message.chat.id, f'Упс, не удалось установить соединение')
        except:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите номер квартиры.')
            await bot.set_state(message.from_user.id, Address.postal_code, message.chat.id)
