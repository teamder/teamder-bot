from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton

from tgbot.middlewares.locale import _


def get_kb():
    keyboard = ReplyKeyboardMarkup(row_width=2)

    keyboard.add(
        KeyboardButton(_("Список пользователей"))
    )
    
    return keyboard
