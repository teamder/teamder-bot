from typing import Dict

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ContentTypes, Message
from aiogram.utils import parts

from tgbot.cb_data import admin_add_conf_cb
from tgbot.handlers.reply import admin_kb
from tgbot.handlers.inline.admin import admin_add_conf_kb
from tgbot.handlers.states.admin.admin_panel import AdminPanelStates
from tgbot.middlewares.locale import _
from tgbot.models.role import UserRole
from tgbot.services.repository import Repo


async def admin_panel(m: Message):
    await m.reply(
        _(
            "Hello {user_name}!\nYou in the admin panel"
        ).format(
            user_name=m.from_user.first_name
        ),
        reply_markup=admin_kb.get_kb()
    )


async def list_users(m: Message, repo: Repo):
    # Get all users from database
    user_list = await repo.list_users()

    # If any user was found
    if user_list:
        msg_text: str = ""

        # Generate message text
        for num, user in enumerate(user_list, start=1):
            username = f"@{user.username}" if user.username is not None else ""
            msg_text += _(
                "{num}. {user_id} "
                "<a href='tg://user?id={user_id}'><b>{fullname}</b></a> "
                "{username}[{date}]\n"
            ).format(
                num=num,
                user_id=user.user_id,
                fullname=user.fullname,
                username=username,
                date=user.created_on
            )

        # If message long than maximum possible message
        # then split message text on parts
        if len(msg_text) > parts.MAX_MESSAGE_LENGTH:
            for message in parts.safe_split_text(
                msg_text, split_separator="\n"
            ):
                await m.answer(message)

        # Else simply send this message text
        else:
            await m.answer(msg_text)

    # If no users was found then send message about it
    else:
        await m.answer(_("No users was found"))


async def list_admins(m: Message, repo: Repo):
    # Get all admins from database
    user_list = await repo.list_admins()

    # If any admin was found
    if user_list:
        msg_text: str = ""

        # Generate message text
        for num, user in enumerate(user_list, start=1):
            msg_text += _(
                "{num}. <a href='tg://user?id={user_id}'>"
                "<b>{user_id}</b></a> [{date}]\n"
            ).format(
                num=num,
                user_id=user.user_id,
                date=user.created_on
            )

        # If message long than maximum possible message
        # then split message text on parts
        if len(msg_text) > parts.MAX_MESSAGE_LENGTH:
            for message in parts.safe_split_text(
                msg_text, split_separator="\n"
            ):
                await m.answer(message)

        # Else simply send this message text
        else:
            await m.answer(msg_text)

    # If no admin was found then send message about it
    else:
        await m.answer(_("No admins was added"))


async def add_admin(m: Message, state: FSMContext):
    # Reseting state
    await state.reset_state()
    # Set add admin state
    await AdminPanelStates.add_admin_state.set()

    # Send message
    await m.answer(
        _(
            "Send user id or forward message "
            "from user who will be an admin"
        )
    )


async def add_admin_handle(m: Message, state: FSMContext):
    try:
        # If message is forwarded take user id from it
        if getattr(m, "forward_from", None):
            user_id = m.forward_from.id

        # Else get user id from message text
        else:
            user_id: int = int(m.text)

    except ValueError:
        await m.reply(
            _(
                "User id is invalid! Forward to me any message "
                "from this user, or send me his id. You can find it, "
                "for example, from the bot @my_id_bot"
            )
        )
        return

    else:
        if user_id < 0:
            await m.reply(
                _(
                    "Forwarded message was not sent by user! "
                    "from this user, or send me his id. You can find it, "
                    "for example, from the bot @my_id_bot"
                )
            )
            return

        else:
            await m.answer(
                _(
                    "Are you sure you want to add user {user_id} as an admin?"
                ).format(
                    user_id=user_id
                ),
                reply_markup=admin_add_conf_kb.get_kb(user_id)
            )


async def add_admin_conf(
    callback: CallbackQuery,
    callback_data: Dict[str, str],
    state: FSMContext,
    repo: Repo
):
    # Get user id from callback data
    user_id: int = int(callback_data.get("user_id"))

    # Add user to admin table
    await repo.add_admin(user_id=user_id)
    # Finish add admin state
    await state.finish()
    # Send success message
    await callback.message.answer(
        _(
            "User {user_id} was added as an admin!"
        ).format(
            user_id=user_id
        )
    )


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_panel, commands=["admin"],
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        list_users, lambda m: m.text == _("List users"),
        state="*", role=UserRole.ADMIN
    )

    dp.register_message_handler(
        list_admins, lambda m: m.text == _("List admins"),
        state="*", role=UserRole.ADMIN
    )

    dp.register_message_handler(
        add_admin, lambda m: m.text == _("Add admin"),
        state="*", role=UserRole.ADMIN
    )
    dp.register_message_handler(
        add_admin_handle, content_types=ContentTypes.ANY,
        state=AdminPanelStates.add_admin_state, role=UserRole.ADMIN
    )
    dp.register_callback_query_handler(
        add_admin_conf, admin_add_conf_cb.filter(),
        state=AdminPanelStates.add_admin_state
    )
    # # or you can pass multiple roles:
    # dp.register_message_handler(
    #     admin_panel, commands=["admin"],
    #     state="*", role=[UserRole.ADMIN]
    # )
    # # or use another filter:
    # dp.register_message_handler(
    #     admin_panel, commands=["admin"],
    #     state="*", is_admin=True
    # )
