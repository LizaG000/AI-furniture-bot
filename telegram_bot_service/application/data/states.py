from telebot.handler_backends import State, StatesGroup

class Products(StatesGroup):
        Categories = State()
        Colors = State()
        Materials = State()
        Products = State()

class Registration(StatesGroup):
        first_name = State()
        middle_name = State()
        last_name = State()
        phone = State()
        email = State()


class Address(StatesGroup):
        country = State()
        region = State()
        city = State()
        street = State()
        house_number = State()
        quadrature_number = State()
        postal_code = State()
        delete_address = State()