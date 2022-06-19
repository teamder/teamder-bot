from typing import Dict

from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.cb_data import example_cb
from tgbot.handlers.inline import example_kb
from tgbot.middlewares.locale import _
from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username
    )

    await m.reply(
        _("Hello, user!"),
        reply_markup=example_kb.get_kb(m.from_user.id)
    )


async def show_user_id(callback: CallbackQuery, callback_data: Dict[str, str]):
    # Get data from callback data
    user_id = callback_data.get("some_data")

    # Answer on callback
    await callback.message.answer(
        _("Your id is {user_id}").format(user_id=user_id)
    )
    # Remove clocks on inline button
    await callback.answer()


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_callback_query_handler(
        show_user_id, example_cb.filter()
    )
