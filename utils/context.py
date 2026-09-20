from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from utils.database import Database

if TYPE_CHECKING:
    from bot import BlopBot

type Interaction = discord.Interaction[BlopBot]


class Context(commands.Context['BlopBot']):
    @property
    def db(self) -> Database:
        return self.bot.db
