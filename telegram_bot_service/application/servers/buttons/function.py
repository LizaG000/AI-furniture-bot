from telebot import types
from application.schemas.users import users
from application.schemas.shop import shop
from application.schemas.states import Products
from application.servers.buttons.buttons import categories_button
from application.servers.buttons.buttons import colors_button
from application.servers.buttons.buttons import materials_button

def button_function(bot):


    @bot.message_handler(func=lambda msg: msg.text == "Отмена")
    async def return_main(message):
        
        state = await bot.get_state(message.from_user.id, message.chat.id)

        if state.startswith("Registration"):
            users[message.chat.id].pop(message.from_user.id)

        await bot.send_message(
            message.chat.id,
            "Операция отменена",
            reply_markup=types.ReplyKeyboardRemove()
        )
        await bot.set_state(message.from_user.id, None, message.chat.id)
    

    
    @bot.message_handler(func=lambda msg: msg.text == "Назад")
    async def before_button(message):
        
        state = await bot.get_state(message.from_user.id, message.chat.id)

        if state == "Products:Categories":
            users[message.chat.id]["categories"] = []
            await bot.send_message(
                message.chat.id,
                "Возвращение в главное меню",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await bot.set_state(message.from_user.id, None, message.chat.id)
        elif state == "Products:Colors":
            users[message.chat.id]["colors"] = []
            await bot.send_message(
                message.chat.id,
                "Выберите категории",
                reply_markup=categories_button()
            )
            await bot.set_state(message.from_user.id, Products.Categories, message.chat.id)
        elif state == "Products:Materials":
            users[message.chat.id]["materials"] = []
            await bot.send_message(
                message.chat.id,
                "Выберите цвета",
                reply_markup=colors_button()
            )
            await bot.set_state(message.from_user.id, Products.Colors, message.chat.id)




    
    @bot.message_handler(func=lambda msg: msg.text == "Продолжить")
    async def do_button(message):
        
        state = await bot.get_state(message.from_user.id, message.chat.id)

        if state == "Products:Categories":
            await bot.send_message(
                message.chat.id,
                "Выберите цвета",
                reply_markup=colors_button()
            )
            await bot.set_state(message.from_user.id, Products.Colors, message.chat.id)
        elif state == "Products:Colors":
            await bot.send_message(
                message.chat.id,
                "Выберите материалы",
                reply_markup=materials_button()
            )
            await bot.set_state(message.from_user.id, Products.Materials, message.chat.id)
        elif state == "Products:Materials":
            users[message.chat.id]["materials"] = []
            await bot.send_message(
                message.chat.id,
                "Подборка продуктов",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await bot.set_state(message.from_user.id, Products.Products, message.chat.id)

