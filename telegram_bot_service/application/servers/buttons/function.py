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
from application.servers.get_bascket import get_bascket
from application.servers.delete_basket import delete_bascket
from application.servers.update_basket import update_bascket
from application.servers.buttons.buttons import basket_message
from application.servers.get_favorites import get_favorites
from application.servers.delete_favorites import delete_favorites
from application.servers.buttons.buttons import favorites_message


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

    async def update_product_message(id_chat: int, id_message: int, index: int, products):
        await bot.delete_message(id_chat, id_message)
        markup = product_message(id_chat, index, products)
        with open(f"images/{products[index].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                id_chat,
                photo,
                caption=f"<b>{products[index].name}</b>\n{products[index].description}\n\nЦена: {products[index].price / 100 * (100-products[index].discount)}₽",
                parse_mode="HTML",
                reply_markup=markup
            )

    async def update_basket_message(id_chat: int, id_message: int, index: int, basket):
        await bot.delete_message(id_chat, id_message)
        markup = basket_message(id_chat, index)
        with open(f"images/{basket[index].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                id_chat,
                photo,
                caption=f"<b>{basket[index].name}</b>\n{basket[index].description}\n\nЦена: {basket[index].price / 100 * (100-basket[index].discount)}₽",
                parse_mode="HTML",
                reply_markup=markup
            )
    
    async def update_favorites_message(id_chat: int, id_message: int, index: int, favorites):
        await bot.delete_message(id_chat, id_message)
        markup = favorites_message(id_chat, index)
        with open(f"images/{favorites[index].images[0]}.png", "rb") as photo:
            await bot.send_photo(
                id_chat,
                photo,
                caption=f"<b>{favorites[index].name}</b>\n{favorites[index].description}\n\nЦена: {favorites[index].price / 100 * (100-favorites[index].discount)}₽",
                parse_mode="HTML",
                reply_markup=markup
            )

    @bot.callback_query_handler(func=lambda call: True)
    async def callback(call):
        id_chat = call.message.chat.id
        # Basket
        if call.data.startswith("left_basket_"):
            index = users[id_chat]["index_basket"]
            basket = users[id_chat]["basket"]
            index = (index - 1) % len(basket)
            users[id_chat]["index_basket"] = index
            await update_basket_message(id_chat, call.message.message_id, index, basket)
        elif call.data.startswith("right_basket_"):
            index = users[id_chat]["index_basket"]
            basket = users[id_chat]["basket"]
            index = (index + 1) % len(basket)
            users[id_chat]["index_basket"] = index
            await update_basket_message(id_chat, call.message.message_id, index, basket)
        elif call.data.startswith("plus_basket_") and users[id_chat]["basket"][users[id_chat]["index_basket"]].count <= users[id_chat]["basket"][users[id_chat]["index_basket"]].product_count:
            index = users[id_chat]["index_basket"]
            print(index)
            print(users[id_chat]["basket"][index])
            basket = users[id_chat]["basket"]
            users[id_chat]["basket"][index].count += 1
            await update_bascket(id_chat=call.message.message_id, id_basket=basket[index].id, count = users[id_chat]["basket"][index].count)
            await update_basket_message(id_chat, call.message.message_id, index, basket)
        elif call.data.startswith("minus_basket_") and users[id_chat]["basket"][users[id_chat]["index_basket"]].count > 0:
            index = users[id_chat]["index_basket"]
            basket = users[id_chat]["basket"]
            users[id_chat]["basket"][index].count -= 1
            await update_bascket(id_chat=call.message.message_id, id_basket=basket[index].id_product, count = users[id_chat]["basket"][index].count)
            await update_basket_message(id_chat, call.message.message_id, index, basket)
        elif call.data.startswith("delete_basket_"):
            index = users[id_chat]["index_basket"]
            basket = users[id_chat]["basket"]
            status = await delete_bascket(id_chat=call.message.message_id, id_basket=basket[index].id)
            print(status)
            if status == 200:
                users[id_chat]["basket"].pop(index)
                if len(basket) != 0:
                    index = index  % len(basket)
                    bot.send_message(id_chat, "Удалено из корзины!")
                    await update_basket_message(id_chat, call.message.message_id, index, basket)
                else:
                    await bot.delete_message(id_chat, call.message.message_id)
                    await bot.send_message(id_chat, "Корзина пуста!")
            else:
                bot.send_message(id_chat, "Ошибка при удалении из корзинs.")
        elif call.data.startswith("left_favorites_"):
            index = users[id_chat]["favorites_index"]
            favorites = users[id_chat]["favorites"]
            index = (index - 1) % len(favorites)
            users[id_chat]["favorites_index"] = index
            await update_favorites_message(id_chat, call.message.message_id, index, favorites)
        elif call.data.startswith("right_favorites_"):
            index = users[id_chat]["favorites_index"]
            favorites = users[id_chat]["favorites"]
            index = (index + 1) % len(favorites)
            users[id_chat]["favorites_index"] = index
            await update_favorites_message(id_chat, call.message.message_id, index, favorites)
        elif call.data.startswith("delete_favorites_"):
            index = users[id_chat]["favorites_index"]
            favorites = users[id_chat]["favorites"]
            status = await delete_favorites(id_chat=call.message.message_id, id_favorites=favorites[index].id)
            if status == 200:
                users[id_chat]["favorites"].pop(index)
                if len(favorites) != 0:
                    index = index  % len(favorites)
                    await bot.send_message(id_chat, "Удалено из избранного!")
                    await update_favorites_message(id_chat, call.message.message_id, index, favorites)
                else:
                    await bot.delete_message(id_chat, call.message.message_id)
                    await bot.send_message(id_chat, "Избранное пусто!")
            else:
                bot.send_message(call.id, "Ошибка при удалении из избранного.")
        elif call.data.startswith("left_"):
            index = users[id_chat]["index"]
            products = users[id_chat]["products"]
            index = (index - 1) % len(products)
            users[id_chat]["index"] = index
            users[id_chat]["count"] = 1
            await update_product_message(id_chat, call.message.message_id, index, products)
        elif call.data.startswith("right_"):
            index = users[id_chat]["index"]
            products = users[id_chat]["products"]
            index = (index + 1) % len(products)
            users[id_chat]["index"] = index
            users[id_chat]["count"] = 1
            await update_product_message(id_chat, call.message.message_id, index, products)
        elif call.data.startswith("plus_") and users[id_chat]["count"] <= users[id_chat]["products"][users[id_chat]["index"]].product_count: 
            index = users[id_chat]["index"]
            products = users[id_chat]["products"]
            users[id_chat]["count"] += 1
            await update_product_message(id_chat, call.message.message_id, index, products)
        elif call.data.startswith("minus_") and users[id_chat]["count"] > 0:
            index = users[id_chat]["index"]
            products = users[id_chat]["products"]
            users[id_chat]["count"] -= 1
            await update_product_message(id_chat, call.message.message_id, index, products)
        elif call.data.startswith("cart_"):
            index = users[id_chat]["index"]
            print(index)
            products = users[id_chat]["products"]
            print(1)
            status = await add_bascket(id_user=users[id_chat][id_chat].id, id_product=products[index].id, count=users[id_chat]["count"])
            print(status)
            if status == 200:
                await bot.send_message(id_chat, "Добавлено в корзину!")
                users[call.message.chat.id]["basket"] = await get_bascket(call.message.chat.id)
            else:
                await bot.send_message(id_chat, "Ошибка при добавлении в корзину.")
        elif call.data.startswith("fav_"):
            index = users[id_chat]["index"]
            products = users[id_chat]["products"]
            status = await add_favorites(id_user=users[id_chat][id_chat].id, id_product=products[index].id)
            if status == 200:
                await bot.send_message(id_chat, "Добавлено в избранное!")
                users[call.message.chat.id]["favorites"] = await get_favorites(call.message.chat.id)
            else:
                await bot.send_message(id_chat, "Ошибка при добавлении в избранное.")
        
    

        
