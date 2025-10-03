import requests
from telegram_bot_service.main import bot
from telegram_bot_service.application.schemas.UserSchemas import CreateUser
from telegram_bot_service.application.servers.validation import validation_str, validation_phone, validation_email
user = CreateUser()


def registration_first_name(message):
    first_name = message.text
    first_name = first_name.lower()
    first_name = validation_str(first_name)
    if not first_name:
        bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста имя.')
        bot.register_next_step_handler(message, registration_first_name)
    else:
        user.id = message.from_user.id
        user.first_name = first_name[0].upper() + first_name[1:]
        bot.send_message(message.chat.id, 'Введите ваше отчество или слово \"Нет\", если у вас нет отчества.')
        bot.register_next_step_handler(message, registration_middle_name)

def registration_middle_name(message):
    middle_name = message.text
    middle_name = middle_name.lower()
    middle_name = validation_str(middle_name)
    if not middle_name:
        bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста отчество или слово \"Нет\".')
        bot.register_next_step_handler(message, registration_middle_name)
    else:
        if middle_name == "нет":
            user.middle_name = None
        else:
            user.middle_name = middle_name[0].upper() + middle_name[1:]
        bot.send_message(message.chat.id, 'Введите вашу фамилию.')
        bot.register_next_step_handler(message, registration_last_name)

def registration_last_name(message):
    last_name = message.text
    last_name = last_name.lower()
    last_name = validation_str(last_name)
    if not last_name:
        bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста фамилию.')
        bot.register_next_step_handler(message, registration_last_name)
    else:
        user.last_name = last_name[0].upper() + last_name[1:]
        bot.send_message(message.chat.id, 'Введите ваш номер телефона в формате 81231231212.')
        bot.register_next_step_handler(message, registration_phone)

def registration_phone(message):
    phone = message.text
    phone = validation_phone(phone)
    if not phone:
        bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста номер телефона.')
        bot.register_next_step_handler(message, registration_phone)
    else:
        user.phone = int(phone)
        bot.send_message(message.chat.id, 'Введите вашу почту.')
        bot.register_next_step_handler(message, registration_email)
        
def registration_email(message):
    email = message.text
    email = email.lower()
    email = validation_email(email)
    if not email:
        bot.send_message(message.chat.id, 'Упс. Кажется вы нажали куда-то не туда.\nВведите пожалуйста вашу почту.')
        bot.register_next_step_handler(message, registration_email)
    else:
        user.email = email
        try:
            requests.post('http://localhost:8000/api/user', data=user)
        except:
            bot.send_message(message.chat.id, f'Упс, не удалось установить соединение')
        bot.send_message(message.chat.id, f'Поздравляю {user.first_name}! Вы успешно зарегистрированы!')
