from telebot import types

def return_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Отмена")
    )
    return markup

