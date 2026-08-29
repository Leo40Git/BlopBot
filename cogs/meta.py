from datetime import datetime

import discord
from discord.ext import commands


class Meta(commands.Cog):
    """Commands relating to Discord or to the bot herself."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='quit', hidden=True)
    @commands.is_owner()
    async def _quit(self, ctx: commands.Context):
        """Quits the bot."""
        await ctx.reply(':wave:')
        await self.bot.close()

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Measures the bot's latency."""
        start_time = datetime.now()
        message = await ctx.reply('Pong!')
        end_time = datetime.now()
        await message.edit(
            content=f'Pong! Latency: {((end_time - start_time).microseconds / 1000) :.2f}ms')


def setup(bot: commands.Bot):
    bot.add_cog(Meta(bot))
