from telebot import types
from application.schemas.shop import shop

def return_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Отмена")
    )
    return markup

def categories_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад")
    )
    markup.add(
        types.KeyboardButton("Продолжить")
    )
    for i in shop["categories_name"]:
        markup.add(
        types.KeyboardButton(i)
    )
    return markup

def colors_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад")
    )
    markup.add(
        types.KeyboardButton("Продолжить")
    )
    for i in shop["colors_name"]:
        markup.add(
        types.KeyboardButton(i)
    )
    return markup

def materials_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад")
    )
    markup.add(
        types.KeyboardButton("Продолжить")
    )
    for i in shop["materials_name"]:
        markup.add(
        types.KeyboardButton(i)
    )
    return markup

