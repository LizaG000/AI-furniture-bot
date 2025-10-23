from telebot import types
from application.schemas.shop import shop
from application.schemas.users import users

def return_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Отмена")
    )
    return markup

def categories_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад"),
        types.KeyboardButton("Продолжить")
    )
    i = 0
    while i < len(shop["categories_name"]):
        markup.row(*[types.KeyboardButton(shop["categories_name"][j]) for j in range(i, min(i+3, len(shop["categories_name"])))])
        i += 3
    return markup

def colors_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад"),
        types.KeyboardButton("Продолжить")
    )
    i = 0
    while i < len(shop["colors_name"]):
        markup.row(*[types.KeyboardButton(shop["colors_name"][j]) for j in range(i, min(i+3, len(shop["colors_name"])))])
        i += 3
    return markup

def materials_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Назад"),
        types.KeyboardButton("Продолжить")
    )
    i = 0
    while i < len(shop["materials_name"]):
        markup.row(*[types.KeyboardButton(shop["materials_name"][j]) for j in range(i, min(i+3, len(shop["materials_name"])))])
        i += 3
    return markup



def product_message(id_chat:int, index: int, products):
    product = products[index]
    markup = types.InlineKeyboardMarkup(row_width=5)
    count = users[id_chat]["count"]

    btn_left = types.InlineKeyboardButton("⬅️", callback_data=f"left_{index}")
    btn_minus = types.InlineKeyboardButton("➖", callback_data=f"minus_{index}")
    btn_count = types.InlineKeyboardButton(f"{count}", callback_data="count")
    btn_plus = types.InlineKeyboardButton("➕", callback_data=f"plus_{index}")
    btn_cart = types.InlineKeyboardButton("🛒", callback_data=f"cart_{index}")
    btn_fav = types.InlineKeyboardButton("💖", callback_data=f"fav_{index}")
    btn_right = types.InlineKeyboardButton("➡️", callback_data=f"right_{index}")

    markup.row(btn_left, btn_minus, btn_count, btn_plus, btn_right)
    markup.row(btn_cart, btn_fav)
    return markup

def basket_message(id_chat:int, index: int):
    count = users[id_chat]["basket"][index].count

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_left = types.InlineKeyboardButton("⬅️", callback_data=f"left_basket_{index}")
    btn_minus = types.InlineKeyboardButton("➖", callback_data=f"minus_basket_{index}")
    btn_count = types.InlineKeyboardButton(f"{count}", callback_data="count")
    btn_plus = types.InlineKeyboardButton("➕", callback_data=f"plus_basket_{index}")
    btn_right = types.InlineKeyboardButton("➡️", callback_data=f"right_basket_{index}")
    btn_delete = types.InlineKeyboardButton("X", callback_data=f"delete_basket_{index}")

    markup.row(btn_left, btn_minus, btn_count, btn_plus, btn_right)
    markup.row(btn_delete)

    return markup

def favorites_message(id_chat:int, index: int):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_left = types.InlineKeyboardButton("⬅️", callback_data=f"left_favorites_{index}")
    btn_right = types.InlineKeyboardButton("➡️", callback_data=f"right_favorites_{index}")
    btn_delete = types.InlineKeyboardButton("X", callback_data=f"delete_favorites_{index}")

    markup.row(btn_left, btn_right)
    markup.row(btn_delete)

    return markup



