from telebot.handler_backends import State, StatesGroup

class Products(StatesGroup):
        Categories = State()
        Colors = State()
        Materials = State()
        Products = State()