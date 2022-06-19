"""This middleware need for bot localisation
run `pybabel extract --input_dir=./tgbot -o locales/teamder-bot.pot` to
extract all locale strings

run `pybabel compile -d locales -D teamder-bot` to compile all
localisation files
"""
from pathlib import Path

from aiogram.contrib.middlewares.i18n import I18nMiddleware

# Name for localisation files
I18N_DOMAIN = "teamder-bot"

# Bot directory
BASE_DIR = Path(__name__).parent
# Locales directory
LOCALES_DIR = BASE_DIR / "locales"

# Localisation middleware
i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)

# Alias for gettext method
_ = i18n.gettext
