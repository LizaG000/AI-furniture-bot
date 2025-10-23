from telebot import types
from application.schemas.users import users
from application.schemas.shop import shop
from application.schemas.states import Products
from application.servers.buttons.buttons import categories_button
from application.servers.buttons.buttons import colors_button
from application.servers.buttons.buttons import materials_button
from application.servers.get_products import get_products
from application.servers.buttons.buttons import product_message
from application.servers.add_bascket import add_bascket
from application.servers.add_favorites import add_favorites



def button_function(bot):


    @bot.message_handler(func=lambda msg: msg.text == "Отмена")
    async def return_main(message):
        
        state = await bot.get_state(message.from_user.id, message.chat.id)

        if state.startswith("Registration"):
            users[message.chat.id].pop(message.chat.id, None)
        elif state.startswith("Address"):
            users[message.chat.id].pop("address", None)

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
            await bot.send_message(
                message.chat.id,
                "Подборка продуктов",
                reply_markup=types.ReplyKeyboardRemove()
            )
            products = await get_products(message.chat.id, bot)
            await bot.set_state(message.from_user.id, None, message.chat.id)


    @bot.callback_query_handler(func=lambda call: True)
    async def callback(call):
        id_chat = call.message.chat.id
        index = users[id_chat]["index"]
        products = users[id_chat]["products"]

        if call.data.startswith("left_"):
            index = (index - 1) % len(products)
            users[id_chat]["count"] = 1
        elif call.data.startswith("right_"):
            index = (index + 1) % len(products)
            users[id_chat]["count"] = 1
        elif call.data.startswith("plus_"):
            users[id_chat]["count"] += 1
        elif call.data.startswith("minus_") and users[id_chat]["count"] > 0:
            users[id_chat]["count"] -= 1
        elif call.data.startswith("cart_"):
            status = await add_bascket(id_user=users[id_chat][id_chat].id, id_product=products[index].id, count=users[id_chat]["count"])
            if status == 200:
                bot.send_message(call.id, "Добавлено в корзину!")
            else:
                bot.send_message(call.id, "Ошибка при добавлении в корзину.")
        elif call.data.startswith("fav_"):
            status = await add_favorites(id_user=users[id_chat][id_chat].id, id_product=products[index].id)
            if status == 200:
                bot.send_message(call.id, "Добавлено в избранное!")
            else:
                bot.send_message(call.id, "Ошибка при добавлении в избранное.")

        users[id_chat]["index"] = index
        await bot.delete_message(id_chat, call.message.message_id)
        markup = product_message(id_chat, index, products)
        with open(f"images/{products[index].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                id_chat,
                photo,
                caption=f"<b>{products[index].name}</b>\n{products[index].description}\n\nЦена: {products[index].price}₽",
                parse_mode="HTML",
                reply_markup=markup
            )
