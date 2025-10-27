import random
from application.data.users import users
from application.servers.buttons.buttons import return_button
from models.model import predict_intent, get_answer, predirect_keras_model
from application.data.output import output
from application.schemas.UserSchemas import CreateUser
from application.servers.input import clearing_input
from application.data.states import Registration
from application.servers.get_addresses import get_addresses_list
from application.data.states import Address
from application.data.states import Products
from application.servers.buttons.buttons import categories_button
from application.servers.get_bascket import get_bascket
from application.servers.buttons.buttons import basket_message
from application.servers.buttons.buttons import favorites_message
from application.servers.get_favorites import get_favorites
from telebot.storage import StateMemoryStorage 
def ii_handlers(bot):

    @bot.message_handler()
    async def ii(message):
        answer = clearing_input(message.text)
        print(answer)
        ii = predirect_keras_model(" ".join(answer))
        print(ii)
        i = random.randint(0, len(output[ii]["output"]) - 1)
        answer = output[ii]["output"][i]
        print(answer)
        if ii == "registration":
            print(1234)
            if message.chat.id not in users:
                users[message.chat.id] = {}
            users[message.chat.id][message.chat.id] = CreateUser()
            await bot.send_message(message.chat.id, output[ii]["output"][i], reply_markup=return_button())
            await bot.set_state(message.from_user.id, Registration.first_name, message.chat.id)
        elif ii == "list_addresses":
            if message.chat.id not in users:
                users[message.chat.id] = {}
            if message.chat.id not in users[message.from_user.id]:
                await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
            else:
                if "text" not in users[message.chat.id] or users[message.chat.id]["text"] == "":
                    await get_addresses_list(message.from_user.id, message.chat.id)
                if users[message.chat.id]["text"] == "":
                    await bot.send_message(message.chat.id, "Упс. Кажется у вас еще нет адресов(")
                else:
                    await bot.send_message(message.chat.id, answer+"\n" + users[message.chat.id]["text"])
        elif ii == "add_address":
            if message.chat.id not in users:
                users[message.chat.id] = {}
            if message.chat.id not in users[message.from_user.id]:
                await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
            else:
                users[message.chat.id]["address"] = {}
                await bot.send_message(message.chat.id, answer, reply_markup=return_button())
                await bot.set_state(message.from_user.id, Address.country, message.chat.id)
        elif ii == "delete_address":
            if message.chat.id not in users:
                users[message.chat.id] = {}
            if message.chat.id not in users[message.from_user.id]:
                await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
            else:
                if "text" not in users[message.chat.id] or users[message.chat.id]["text"] == "":
                    await get_addresses_list(message.from_user.id, message.chat.id)
                if users[message.chat.id]["text"] == "":
                    await bot.send_message(message.chat.id, "Упс. Кажется у вас еще нет адресов(")
                else:
                    answer = answer + users[message.chat.id]["text"]
                    await bot.send_message(message.chat.id, answer, reply_markup=return_button())
                    await bot.set_state(message.from_user.id, Address.delete_address, message.chat.id)
        elif ii == "catalog":
            if message.chat.id not in users:
                users[message.chat.id] = {}
            users[message.chat.id]["categories"] = []
            users[message.chat.id]["materials"] = []
            users[message.chat.id]["colors"] = []
            await bot.send_message(message.chat.id, answer, reply_markup=categories_button())
            await bot.set_state(message.from_user.id, Products.Categories, message.chat.id)
        elif ii == "basket":
            print(users)
            if message.chat.id not in users:
                users[message.chat.id] = {}

            print(users)
            users[message.chat.id]["basket"] = await get_bascket(message.chat.id)
            basket = users[message.chat.id]["basket"]
            if basket == []:
                print(1)
                await bot.send_message(message.chat.id, 'У вас пусто в корзине.')
            else:
                
                print(2)
                users[message.chat.id]["index_basket"] = 0
                print(users[message.chat.id])
                await bot.send_message(message.chat.id, answer)
                with open(f"images/{basket[0].images[0]}.png", "rb") as photo:
                    await bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=f"<b>{basket[0].name}</b>\n{basket[0].description}\n\nЦена: {basket[0].price / 100 * (100-basket[0].discount)}₽",
                        parse_mode="HTML",
                        reply_markup=basket_message(message.chat.id, 0)
                    )
        elif ii == "favorites":
            if message.chat.id not in users:
                users[message.chat.id] = {}
                
                await bot.send_message(message.chat.id, "Упс. Кажется вы еще не зарегистрированы(")
            users[message.chat.id]["favorites"] = await get_favorites(message.chat.id)
            favorites = users[message.chat.id]["favorites"]
            if favorites == []:
                await bot.send_message(message.chat.id, 'У вас пусто в избранном.')
            else:
                users[message.chat.id]["favorites_index"] = 0
                await bot.send_message(message.chat.id, 'Ваши товары')
                with open(f"images/{favorites[0].images[0]}.png", "rb") as photo:
                    await bot.send_photo(
                        message.chat.id,
                        photo,
                        caption=f"<b>{favorites[0].name}</b>\n{favorites[0].description}\n\nЦена: {favorites[0].price / 100 * (100-favorites[0].discount)}₽",
                        parse_mode="HTML",
                        reply_markup=favorites_message(message.chat.id, 0)
                    )
        elif ii == "not_understood":
            answer = get_answer(" ".join(answer))
            await bot.send_message(message.chat.id, answer)
        else:
            await bot.send_message(message.chat.id, output[ii]["output"][i])