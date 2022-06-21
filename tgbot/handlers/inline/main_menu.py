from aiogram.types.inline_keyboard import InlineKeyboardButton, \
    InlineKeyboardMarkup

from tgbot.cb_data import main_menu_cb
from tgbot.middlewares.locale import _


def get_kb(user_id: int) -> InlineKeyboardMarkup:
    # Create keyboard
    keyboard = InlineKeyboardMarkup(row_width=1)

    # Add button with text and callback data
    keyboard.add(
        InlineKeyboardButton(
            text=_("Projects"),
            callback_data=main_menu_cb.new(
                menu="projects"
            )
        ),
        InlineKeyboardButton(
            text=_("New project"),
            callback_data=main_menu_cb.new(
                menu="new_project"
            )
        ),
        InlineKeyboardButton(
            text=_("Overview"),
            callback_data=main_menu_cb.new(
                menu="overview"
            )
        ),
        InlineKeyboardButton(
            text=_("Settings"),
            callback_data=main_menu_cb.new(
                menu="settings"
            )
        ),
    )

    # Return keyboard
    return keyboard
