from telebot import types

def button_function(bot):
    @bot.message_handler(func=lambda msg: msg.text == "Отмена")
    async def return_main(message):
        # 1️⃣ Убираем клавиатуру и сообщаем пользователю
        await bot.send_message(
            message.chat.id,
            "Операция отменена ❌",
            reply_markup=types.ReplyKeyboardRemove()
        )

        # 2️⃣ Сбрасываем состояние
        await bot.set_state(message.from_user.id, None, message.chat.id)