from telebot import types
from application.schemas.users import users

def button_function(bot):
    @bot.message_handler(func=lambda msg: msg.text == "Отмена")
    async def return_main(message):
        
        state = await bot.get_state(message.from_user.id, message.chat.id)

        if state.startswith("Registration"):
            users.pop(message.chat.id)

        await bot.send_message(
            message.chat.id,
            "Операция отменена",
            reply_markup=types.ReplyKeyboardRemove()
        )


        await bot.set_state(message.from_user.id, None, message.chat.id)