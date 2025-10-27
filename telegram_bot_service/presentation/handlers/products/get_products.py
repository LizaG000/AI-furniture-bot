from application.servers.get_addresses import get_addresses_list
from application.data.users import users
from application.data.shop import shop
from application.data.states import Products
from application.servers.buttons.buttons import categories_button



def get_products_handlers(bot):

    @bot.message_handler(commands=['search_product', 'get_products', 'catalog'])
    async def search_product(message):
        if message.chat.id not in users:
            users[message.chat.id] = {}
        users[message.chat.id]["categories"] = []
        users[message.chat.id]["materials"] = []
        users[message.chat.id]["colors"] = []
        await bot.send_message(message.chat.id, "Выберите категорию товаров.", reply_markup=categories_button())
        await bot.set_state(message.from_user.id, Products.Categories, message.chat.id)


    @bot.message_handler(state=Products.Categories)
    async def categories(message):
        text = message.text[0].upper() + message.text[1:]
        if text in shop["categories_name"]:
            if text not in users[message.chat.id]["categories"]:
                users[message.chat.id]["categories"].append(text)
                categories = ", ".join(users[message.chat.id]["categories"])
                await bot.send_message(message.chat.id, f"Вы добавили категорию {text}.\nВесь список выбранных категорий: {categories}.")
            else:
                users[message.chat.id]["categories"].pop(users[message.chat.id]["categories"].index(text))
                if users[message.chat.id]["categories"] == []:
                    await bot.send_message(message.chat.id, f"Вы удалили категорию {text}.\nУ вас нет выбронных категорий.")
                else:
                    categories = ", ".join(users[message.chat.id]["categories"])
                    await bot.send_message(message.chat.id, f"Вы удалили категорию {text}.\nВесь список выбранных категорий: {categories}.")
        else:
            await bot.send_message(message.chat.id, "Упс, кажется у нас нет такой категории(")


    @bot.message_handler(state=Products.Colors)
    async def colors(message):
        text = message.text[0].upper() + message.text[1:]
        if text in shop["colors_name"]:
            if text not in users[message.chat.id]["colors"]:
                users[message.chat.id]["colors"].append(text)
                colors = ", ".join(users[message.chat.id]["colors"])
                await bot.send_message(message.chat.id, f"Вы добавили цвет {text}.\nВесь список выбранных цветов: {colors}.")
            else:
                users[message.chat.id]["colors"].pop(users[message.chat.id]["colors"].index(text))
                if users[message.chat.id]["colors"] == []:
                    await bot.send_message(message.chat.id, f"Вы удалили категорию {text}.\nУ вас нет выбронных цветов.")
                else:
                    colors = ", ".join(users[message.chat.id]["colors"])
                    await bot.send_message(message.chat.id, f"Вы удалили цвет {text}.\nВесь список выбранных цветов: {colors}.")
        else:
            await bot.send_message(message.chat.id, "Упс, кажется у нас нет таких цветов(")


    @bot.message_handler(state=Products.Materials)
    async def materials(message):
        text = message.text[0].upper() + message.text[1:]
        if text in shop["materials_name"]:
            if text not in users[message.chat.id]["materials"]:
                users[message.chat.id]["materials"].append(text)
                materials = ", ".join(users[message.chat.id]["materials"])
                await bot.send_message(message.chat.id, f"Вы добавили материал {text}.\nВесь список выбранных материалов: {materials}.")
            else:
                users[message.chat.id]["materials"].pop(users[message.chat.id]["materials"].index(text))
                if users[message.chat.id]["materials"] == []:
                    await bot.send_message(message.chat.id, f"Вы удалили категорию {text}.\nУ вас нет выбронных материалов.")
                else:
                    materials = ", ".join(users[message.chat.id]["materials"])
                    await bot.send_message(message.chat.id, f"Вы удалили материал {text}.\nВесь список выбранных материалов: {materials}.")
        else:
            await bot.send_message(message.chat.id, "Упс, кажется у нас нет таких материалов(")
    
    