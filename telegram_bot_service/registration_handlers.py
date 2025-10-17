# from application.servers.registrtation import registration_first_name
import aiohttp
import json
from telebot.asyncio_storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from application.schemas.UserSchemas import CreateUser
from application.servers.validation import validation_str, validation_phone, validation_email
user = CreateUser()
user_data = {}
def registration_handlers(bot):
    class Registration(StatesGroup):
        first_name = State()
        middle_name = State()
        last_name = State()
        phone = State()
        email = State()
    @bot.message_handler(commands=['start'])
    async def main(message):
        await bot.send_message(message.chat.id, 'Привет! 👋 Добро пожаловать в мебельный магазин <b>«Future»</b>.\nЗарегистрируйтесь — и мы сохраним ваши любимые товары и предложим персональные скидки!\nЧтобы зарегистрироваться введите /registrate', parse_mode='html')

    @bot.message_handler(commands=['registrate', 'регистрация'])
    async def registration_name(message):
        print("УРАААА")
        await bot.send_message(message.chat.id, 'Введите ваше имя.')
        await bot.set_state(message.from_user.id, Registration.first_name, message.chat.id)

    @bot.message_handler(state=Registration.first_name)
    async def registration_first_name(message):
        first_name = message.text
        first_name = first_name.lower()
        first_name = validation_str(first_name)
        if not first_name:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста имя.')
            await bot.set_state(message.from_user.id, Registration.first_name, message.chat.id)
        else:
            user.id = message.from_user.id
            user.first_name = first_name[0].upper() + first_name[1:]
            await bot.send_message(message.chat.id, 'Введите ваше отчество или слово \"Нет\", если у вас нет отчества.')
            await bot.set_state(message.from_user.id, Registration.middle_name, message.chat.id)

    @bot.message_handler(state=Registration.middle_name)
    async def registration_middle_name(message):
        middle_name = message.text
        middle_name = middle_name.lower()
        middle_name = validation_str(middle_name)
        if not middle_name:
            await bot.send_message(message.chat.id,
                             'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста отчество или слово \"Нет\".')
            await bot.set_state(message.from_user.id, Registration.middle_name, message.chat.id)
        else:
            if middle_name == "нет":
                user.middle_name = None
            else:
                user.middle_name = middle_name[0].upper() + middle_name[1:]
            await bot.send_message(message.chat.id, 'Введите вашу фамилию.')
            await bot.set_state(message.from_user.id, Registration.last_name, message.chat.id)


    @bot.message_handler(state=Registration.last_name)
    async def registration_last_name(message):
        last_name = message.text
        last_name = last_name.lower()
        last_name = validation_str(last_name)
        if not last_name:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста фамилию.')
            await bot.set_state(message.from_user.id, Registration.last_name, message.chat.id)
        else:
            user.last_name = last_name[0].upper() + last_name[1:]
            await bot.send_message(message.chat.id, 'Введите ваш номер телефона в формате 81231231212.')
            await bot.set_state(message.from_user.id, Registration.phone, message.chat.id)

    @bot.message_handler(state=Registration.phone)
    async def registration_phone(message):
        phone = message.text
        phone = validation_phone(phone)
        if not phone:
            await bot.send_message(message.chat.id,
                             'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста номер телефона.')
            await bot.set_state(message.from_user.id, Registration.phone, message.chat.id)
        else:
            user.phone =  int(phone)
            await bot.send_message(message.chat.id, 'Введите вашу почту.')
            await bot.set_state(message.from_user.id, Registration.email, message.chat.id)

    @bot.message_handler(state=Registration.email)
    async def registration_email(message):
        email = message.text
        email = email.lower()
        email = validation_email(email)
        if not email:
            await bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста вашу почту.')
            await bot.set_state(message.from_user.id, Registration.email, message.chat.id)
        else:
            user.email = email
            async with aiohttp.ClientSession() as session:
                data = user.__dict__
                print(data)
                result = await session.post('http://future-backend.tw1.ru:8003/api/user', json=data)
                print(result)
                print(await result.text())
                await bot.send_message(message.chat.id, f'Поздравляю {result.first_name}! Вы успешно зарегистрированы!')
            # try:
            #     async with aiohttp.ClientSession() as session:
            #         data = user.model_dump()
            #         print(data)
            #         result = await session.post('http://future-backend.tw1.ru:8003/api/user', json=data)
            #         print(result)
            #         print(result.text)
            #         await bot.send_message(message.chat.id, f'Поздравляю {result.first_name}! Вы успешно зарегистрированы!')
            # except:
            #     await bot.send_message(message.chat.id, f'Упс, не удалось установить соединение')
