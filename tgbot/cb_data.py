"""Create callback data for inline keyboards"""
from aiogram.utils.callback_data import CallbackData

# Callback data just for example
example_cb = CallbackData("example", "some_data")
cancel_cb = CallbackData("cancel")
admin_add_conf_cb = CallbackData("admin_add_conf", "user_id")
admin_delete_conf_cb = CallbackData("admin_delete_conf", "user_id")
