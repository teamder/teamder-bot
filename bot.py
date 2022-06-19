import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.engine import AsyncEngine
from sqlalchemy.pool import QueuePool

from tgbot.config import load_config
from tgbot.database.tables import metadata
from tgbot.filters.role import RoleFilter, AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.user import register_user
from tgbot.middlewares.db import DbMiddleware
from tgbot.middlewares.role import RoleMiddleware
from tgbot.middlewares.locale import i18n

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    load_dotenv(".env")


async def create_pool(database_url: str, echo: bool) -> AsyncEngine:
    """Create connection pool to database

    :param database_url: Database url
    :type database_url: str
    :param echo: Echo parameter
    :type echo: bool
    :return: Async connection pool
    :rtype: AsyncEngine
    """
    engine = create_async_engine(
        database_url, pool_size=20, max_overflow=0,
        poolclass=QueuePool, echo=echo
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    return engine


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.error("Starting bot")
    config = load_config()

    if config.tg_bot.use_redis:
        storage = RedisStorage2()
    else:
        storage = MemoryStorage()
    pool = await create_pool(
        database_url=config.db.database_url,
        echo=False,
    )

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(DbMiddleware(pool))
    dp.middleware.setup(RoleMiddleware(config.tg_bot.admin_list))
    dp.middleware.setup(i18n)
    dp.filters_factory.bind(RoleFilter)
    dp.filters_factory.bind(AdminFilter)

    register_admin(dp)
    register_user(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
