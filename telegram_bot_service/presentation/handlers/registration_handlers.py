import aiohttp
from telebot.asyncio_storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup
from application.schemas.UserSchemas import CreateUser
from application.servers.validation import validation_str, validation_phone, validation_email
from application.schemas.users import users
from application.servers.buttons.buttons import return_button
from telebot import types

def registration_handlers(bot):
    class Registration(StatesGroup):
        first_name = State()
        middle_name = State()
        last_name = State()
        phone = State()
        email = State()

    @bot.message_handler(commands=['start'])
    async def main(message):
        users[message.chat.id] = {}
        await bot.send_message(message.chat.id, 'Привет! 👋 Добро пожаловать в мебельный магазин <b>«Future»</b>.\nЗарегистрируйтесь — и мы сохраним ваши любимые товары и предложим персональные скидки!\nЧтобы зарегистрироваться введите /registrate', parse_mode='html')

    @bot.message_handler(commands=['registrate', 'регистрация'])
    async def registration_name(message):
        if message.chat.id not in users:
            users[message.chat.id] = {}
        users[message.chat.id][message.chat.id] = CreateUser()
        await bot.send_message(message.chat.id, 'Введите ваше имя.', reply_markup=return_button())
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
            users[message.chat.id][message.chat.id].id = message.from_user.id
            users[message.chat.id][message.chat.id].first_name = first_name[0].upper() + first_name[1:]
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
                users[message.chat.id][message.chat.id].middle_name = None
            else:
                users[message.chat.id][message.chat.id].middle_name = middle_name[0].upper() + middle_name[1:]
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
            users[message.chat.id][message.chat.id].last_name = last_name[0].upper() + last_name[1:]
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
            users[message.chat.id][message.chat.id].phone =  int(phone)
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
            users[message.chat.id][message.chat.id].email = email
            print(users[message.chat.id][message.chat.id])
            try:
                async with aiohttp.ClientSession() as session:
                    data = users[message.chat.id][message.chat.id].__dict__
                    await session.post('http://future-backend.tw1.ru:8003/api/user', json=data)
                    await bot.send_message(message.chat.id, f'Поздравляю {users[message.chat.id][message.chat.id].first_name}! Вы успешно зарегистрированы!', reply_markup=types.ReplyKeyboardRemove())
                    await bot.set_state(message.from_user.id, None, message.chat.id)
            except:
                await bot.send_message(message.chat.id, f'Упс, не удалось установить соединение')
                users.pop(message.chat.id)
