from datetime import datetime

import discord
from discord.ext import commands

from bot import BlopBot


class Meta(commands.Cog):
    """Commands relating to Discord or to the bot herself."""

    def __init__(self, bot: BlopBot):
        self.bot = bot

    @commands.command(name='quit', aliases=['exit', 'shutdown'], hidden=True)
    @commands.is_owner()
    async def _quit(self, ctx: commands.Context):
        """Quits the bot."""
        await ctx.reply('<a:localbotdies:1543287537710403615>')
        await self.bot.close()

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Measures the bot's latency."""
        start_time = datetime.now()
        message = await ctx.send('Pong!')
        end_time = datetime.now()
        await message.edit(
            content=f'Pong! Latency: {((end_time - start_time).microseconds / 1000) :.2f}ms')

    @commands.group(hidden=True)
    @commands.is_owner()
    async def ext(self, ctx: commands.Context):
        """Manage extensions."""
        pass

    @ext.command(name='load')
    async def ext_load(self, ctx: commands.Context, *, package: str):
        """
        Loads an extension.
        """
        try:
            await self.bot.load_extension(package)
        except commands.ExtensionError as e:
            await ctx.reply(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.reply(':ok_hand:')

    @ext.command(name='unload')
    async def ext_unload(self, ctx: commands.Context, *, package: str):
        """
        Unloads an extension.
        """
        try:
            await self.bot.unload_extension(package)
        except commands.ExtensionError as e:
            await ctx.reply(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.reply(':ok_hand:')

    @ext.command(name='reload')
    async def ext_reload(self, ctx: commands.Context, *, package: str):
        """
        Reloads an extension.
        """
        try:
            await self.bot.reload_extension(package)
        except commands.ExtensionError as e:
            await ctx.reply(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.reply(':ok_hand:')

    @ext.command(name='reloadall')
    async def ext_reload_all(self, ctx: commands.Context):
        """
        Reloads all extensions.
        """
        packages = list(self.bot.extensions.keys())
        statuses: list[tuple[bool, str]] = []

        for package in packages:
            try:
                await self.bot.reload_extension(package)
            except commands.ExtensionError:
                # TODO log this somewhere
                statuses.append((False, package))
            else:
                statuses.append((True, package))

        await ctx.reply('\n'.join(
            f'{':white_check_mark:' if status else ':x:'}: `{package}`' for status, package in statuses))


async def setup(bot: BlopBot):
    await bot.add_cog(Meta(bot))
