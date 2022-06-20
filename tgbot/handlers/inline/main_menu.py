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
            text=_("Projects"),
            callback_data=example_cb.new(
                some_data=user_id
            )
        ),
        InlineKeyboardButton(
            text=_("New project"),
            callback_data=example_cb.new(
                some_data=user_id
            )
        ),
        InlineKeyboardButton(
            text=_("Overview"),
            callback_data=example_cb.new(
                some_data=user_id
            )
        ),
        InlineKeyboardButton(
            text=_("Settings"),
            callback_data=example_cb.new(
                some_data=user_id
            )
        ),
    )

    # Return keyboard
    return keyboard