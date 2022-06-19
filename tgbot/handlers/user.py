from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.handlers.inline import example_kb
from tgbot.middlewares.locale import _
from tgbot.services.repository import Repo


async def user_start(m: Message, repo: Repo):
    await repo.add_user(
        user_id=m.from_user.id,
        firstname=m.from_user.first_name,
        lastname=m.from_user.last_name,
        fullname=m.from_user.full_name
    )

    await m.reply(
        _("Hello, user!"),
        reply_markup=example_kb.get_kb(m.from_user.id)
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
