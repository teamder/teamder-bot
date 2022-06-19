from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.cb_data import example_cb, cancel_cb
from tgbot.handlers.inline import example_kb
from tgbot.middlewares.locale import _
from tgbot.services.repository import Repo


async def cancel_handler(callback: CallbackQuery, state: FSMContext):
    # Reset state
    await state.reset_state()
    # Remove message
    await callback.message.delete()
    # Send message about cancel action
    await callback.message.answer(_("Action was canceled"))


async def user_start(m: Message, repo: Repo):
    # Add user to database
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        fullname=m.from_user.full_name,
        lastname=m.from_user.last_name,
        username=m.from_user.username
    )

    # Send message to user with inline example keyboard
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
    # User start
    dp.register_message_handler(user_start, commands=["start"], state="*")

    # Example callback handler
    dp.register_callback_query_handler(
        show_user_id, example_cb.filter()
    )

    # Cancel callback handler
    dp.register_callback_query_handler(
        cancel_handler, cancel_cb.filter(), state="*"
    )
