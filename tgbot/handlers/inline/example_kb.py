"""Example of inline keyboard. Callback data is neccessary"""
from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup

from tgbot.cb_data import example_cb
from tgbot.middlewares.locale import _


def get_kb(user_id: int) -> InlineKeyboardMarkup:
    # Create keyboard
    keyboard = InlineKeyboardMarkup(row_width=1)

    # Add button with text and callback data
    keyboard.add(
        InlineKeyboardButton(
            text=_("Show my id"),
            callback_data=example_cb.new(
                some_data=user_id
            )
        )
    )

    # Return keyboard
    return keyboard
