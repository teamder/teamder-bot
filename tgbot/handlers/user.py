"""User main handlers"""
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils import parts

from tgbot.cb_data import cancel_cb, main_menu_cb
from tgbot.handlers.inline import main_menu
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
        _("Teamder main menu"),
        reply_markup=main_menu.get_kb(m.from_user.id)
    )


async def show_user_projects(callback: CallbackQuery, repo: Repo):
    # Get all user projects
    projects = await repo.get_users_projects(callback.from_user.id)

    # If user don't have any projects - return
    if not projects:
        await callback.message.answer(
            _("You don't have any projects yet")
        )
        return

    # Else generate message text with info about every project
    msg_text = ""
    for num, project in enumerate(projects, start=1):
        msg_text += _(
            "{num}. {name} - {desc} [{created_on}]\n"
        ).format(
            num=num,
            name=project.name,
            desc=project.description.replace("\n", ""),
            created_on=project.created_on
        )

    # Message text length is longer than maximum posible
    if len(msg_text) > parts.MAX_MESSAGE_LENGTH:
        # Safe split message on parts with split separator as new line
        for msg in parts.safe_split_text(msg_text, split_separator="\n"):
            # Send every part of messsage
            await callback.message.answer(msg)

    # Else send all message text without spliting
    else:
        await callback.message.answer(msg_text)


def register_user(dp: Dispatcher):
    # User start
    dp.register_message_handler(user_start, commands=["start"], state="*")

    # Cancel callback handler
    dp.register_callback_query_handler(
        cancel_handler, cancel_cb.filter(), state="*"
    )

    # Show user projects callback handler
    dp.register_callback_query_handler(
        show_user_projects, main_menu_cb.filter(menu="projects"),
        state="*"
    )
