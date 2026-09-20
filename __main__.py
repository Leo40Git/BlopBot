import asyncio
import contextlib
import logging
from logging.handlers import RotatingFileHandler

import discord
from dotenv import dotenv_values
from pymongo import AsyncMongoClient

from bot import BlopBot
from utils.database import Database


class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__(name='discord.state')

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname == 'WARNING' and 'referencing an unknown' in record.msg:
            return False
        return True


@contextlib.contextmanager
def setup_logging():
    privlog = logging.getLogger()

    try:
        discord.utils.setup_logging()
        # __enter__
        max_bytes = 32 * 1024 * 1024  # 32 MiB
        logging.getLogger('discord').setLevel(logging.INFO)
        logging.getLogger('discord.http').setLevel(logging.WARNING)
        logging.getLogger('discord.state').addFilter(RemoveNoise())

        privlog.setLevel(logging.INFO)
        handler = RotatingFileHandler(filename='blopbot.log', encoding='utf-8', mode='w', maxBytes=max_bytes, backupCount=5)
        dt_fmt = '%Y-%m-%d %H:%M:%S'
        fmt = logging.Formatter('[{asctime}] [{levelname:<7}] {name}: {message}', dt_fmt, style='{')
        handler.setFormatter(fmt)
        privlog.addHandler(handler)

        yield
    finally:
        # __exit__
        handlers = privlog.handlers[:]
        for handler in handlers:
            handler.close()
            privlog.removeHandler(handler)


async def run_bot():
    config = dotenv_values(".env")

    log = logging.getLogger()

    try:
        db = Database(config['DB_URL'])
        await db.migrate()
    except Exception as e:
        log.exception('Could not set up MongoDB client, exiting',
                      exc_info=e)
        return

    async with db:
        async with BlopBot(db) as bot:
            await bot.start(config['TOKEN'], reconnect=True)


with setup_logging():
    asyncio.run(run_bot())
