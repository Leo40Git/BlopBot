from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from discord import User, Member, AllowedMentions, app_commands, Interaction, AppCommandType
from discord.ext import commands
from discord.ext.commands import Author
from pymongo.asynchronous.collection import AsyncCollection

from bot import BlopBot
from utils.context import Context
from utils.converters import ZoneInfoConverter
from utils.database import UserSettings


class Time(commands.Cog):
    """Commands relating to dates, times, and timezones."""

    def __init__(self, bot: BlopBot):
        self.bot = bot

        self.context_commands = [
            app_commands.ContextMenu(
                name='Get local time',
                callback=self.time_context_menu_callback
            )
        ]

        for command in self.context_commands:
            self.bot.tree.add_command(command)

    async def cog_unload(self):
        for command in self.context_commands:
            self.bot.tree.remove_command(command.name, type=command.type)

    @commands.command()
    async def settimezone(
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

        settings = await ctx.get_user_settings(ctx.author)
        settings['tz_key'] = tz.key
        await ctx.set_user_settings(settings)

        # TODO better timezone name?
        await ctx.send(f'Your timezone has been set to `{tz}`.')

    @commands.command()
    async def time(
            self,
            ctx: Context,
            target: Member | User = Author
    ):
        """
        Gets the current local time in the specified user's timezone.

        Parameters
        ----------
        ctx
        target
            The target user.

        """

        settings = await ctx.get_user_settings(target)
        tz_key = settings.get('tz_key')

        if tz_key is None:
            await ctx.send(f'{target.mention} has not specified their timezone. '
                           f'This can be done with the !settimezone command.',
                           allowed_mentions=AllowedMentions.none())
            return

        tz: ZoneInfo
        try:
            tz = ZoneInfo(tz_key)
        except ValueError, ZoneInfoNotFoundError:
            # TODO
            return

        now = datetime.now(tz)
        await ctx.send(f'It is currently {now.strftime('%H:%M')} for {target.mention}.',
                       allowed_mentions=AllowedMentions.none())

    async def time_context_menu_callback(
            self,
            interaction: Interaction,
            user: Member | User
    ):
        # no Context, so...
        c: AsyncCollection[UserSettings] = self.bot.db['user-settings']
        settings = await c.find_one({'_id': user.id})
        if settings is None:
            settings = UserSettings(_id=user.id)

        tz_key = settings.get('tz_key')

        # this is... very much reachable? pycharmpls
        # noinspection unreachable-code
        if tz_key is None:
            await interaction.response.send_message(
                f'{user.mention} has not specified their timezone. '
                f'This can be done with the !settimezone command.',
                ephemeral=True)
            return

        tz: ZoneInfo
        try:
            tz = ZoneInfo(tz_key)
        except ValueError, ZoneInfoNotFoundError:
            # TODO
            return

        now = datetime.now(tz)
        await interaction.response.send_message(
            f'It is currently {now.strftime('%H:%M')} for {user.mention}.',
            ephemeral=True)


async def setup(bot: BlopBot):
    await bot.add_cog(Time(bot))
