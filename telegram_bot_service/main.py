import telebot

bot = telebot.TeleBot("8391809243:AAGi-OMZxGl3PnAuMeIW-xDi0UntJEes-vM")

if __name__ == '__main__':
    bot.polling(non_stop=True)