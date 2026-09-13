from zoneinfo import ZoneInfo

from discord.ext import commands

from bot import BlopBot
from utils.context import Context
from utils.converters import ZoneInfoConverter


class Time(commands.Cog):
    """Commands relating to dates, times, and timezones."""

    @commands.command('settimezone')
    async def set_timezone(
            self,
            ctx: Context,
            tz: ZoneInfo = commands.parameter(converter=ZoneInfoConverter)):
        """
        Sets your timezone.

        This information is used to convert times from your local timezone to BlopBot's timezone
        when you use them as arguments for commands.

        Parameters
        ----------
        ctx
        tz
            The timezone to change to.
        """

        # TODO
        await ctx.send(f'UH HELLO????? {tz}')

        entity = await ctx.read_user_entity(ctx.author)
        entity['tz_key'] = tz.key
        await ctx.update_user_entity(entity)


async def setup(bot: BlopBot):
    await bot.add_cog(Time())
