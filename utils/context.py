from typing import TYPE_CHECKING

from discord.ext import commands
from pymongo.asynchronous.database import AsyncDatabase

if TYPE_CHECKING:
    from bot import BlopBot


class Context(commands.Context[BlopBot]):
    @property
    def db(self) -> AsyncDatabase:
        return self.bot.db
