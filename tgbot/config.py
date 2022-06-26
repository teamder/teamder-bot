"""Contains dataclasses of config data"""
from os import getenv
from dataclasses import dataclass
from typing import List


@dataclass
class DbConfig:
    database_url: str


@dataclass
class TgBot:
    token: str
    admin_list: List[int]
    use_redis: bool


@dataclass
class RedisConfig:
    url: str


@dataclass
class WebhookConfig:
    domain: str
    path: str
    host: str
    port: int


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    redis: RedisConfig
    webhook: WebhookConfig


def cast_bool(value: str) -> bool:
    """Format string value to bool

    :param value: String true, t, 1 or yes
    :type value: str
    :return: Returns True or False
    :rtype: bool
    """
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config():
    """Returns Config class with settings of
    telegram bot, database and Redis

    :return: Config class
    :rtype: Config
    """
    return Config(
        tg_bot=TgBot(
            token=getenv("BOT_TOKEN"),
            admin_list=[int(x.strip()) for x in getenv("ADMIN_ID").split(",")],
            use_redis=cast_bool(getenv("USE_REDIS")),
        ),
        db=DbConfig(
            database_url=getenv("DATABASE_URL").replace(
                "postgres://", "postgresql+asyncpg://"
            )
        ),
        redis=RedisConfig(url=getenv("REDIS_URL")),
        webhook=WebhookConfig(
            domain=getenv("WEBHOOK_DOMAIN"),
            path=getenv("WEBHOOK_PATH"),
            host=getenv("HOST"),
            port=int(getenv("PORT", default=5000))
        )
    )
