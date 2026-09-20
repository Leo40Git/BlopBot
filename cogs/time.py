from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from discord import User, Member, AllowedMentions, app_commands
from discord.ext import commands
from discord.ext.commands import Author

from bot import BlopBot
from utils.context import Interaction, Context
from utils.converters import ZoneInfoConverter


class Time(commands.Cog):
    """Commands relating to dates, times, and timezones."""

    def __init__(self, bot: BlopBot):
        self.bot = bot

        self.context_menus = [
            app_commands.ContextMenu(
                name='Get local time',
                callback=self.time_context_menu_callback
            )
        ]

    async def cog_load(self):
        for command in self.context_menus:
            self.bot.tree.add_command(command)

    async def cog_unload(self):
        for command in self.context_menus:
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

        settings = await ctx.bot.db.get_user_settings(ctx.author)
        settings['tz_key'] = tz.key
        await ctx.bot.db.save_user_settings(settings)

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

        settings = await ctx.bot.db.get_user_settings(target)
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
            target: Member | User
    ):
        settings = await interaction.client.db.get_user_settings(target)
        tz_key = settings.get('tz_key')

        # this is... very much reachable? pycharmpls
        # noinspection unreachable-code
        if tz_key is None:
            await interaction.response.send_message(
                f'{target.mention} has not specified their timezone. '
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
            f'It is currently {now.strftime('%H:%M')} for {target.mention}.',
            ephemeral=True)


async def setup(bot: BlopBot):
    await bot.add_cog(Time(bot))
