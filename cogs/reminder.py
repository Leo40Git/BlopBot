from discord.ext import commands

from bot import BlopBot
from utils.context import Context


class Reminder(commands.Cog):
    """Commands relating to reminders."""

    @commands.command(aliases=['remind', 'remindme'])
    async def reminder(
            self,
            ctx: Context
    ):
        pass


async def setup(bot: BlopBot):
    await bot.add_cog(Reminder())
