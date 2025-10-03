from telegram_bot_service.main import bot
from telegram_bot_service.application.servers.registrtation import registration_first_name

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, 'Привет! 👋 Добро пожаловать в мебельный магазин <b>«Future»</b>.\nЗарегистрируйтесь — и мы сохраним ваши любимые товары и предложим персональные скидки!\nЧтобы зарегистрироваться введите /registrate', parse_mode='html')

@bot.message_handler(commands=['registrate', 'регистрация'])
def registration_name(message):
    bot.send_message(message.chat.id, 'Введите ваше имя.')
    bot.register_next_step_handler(message, registration_first_name)

bot.polling(non_stop=True)