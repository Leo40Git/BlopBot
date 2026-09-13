import asyncio
from random import choice, randrange

import discord
from discord.ext import commands

from bot import BlopBot


class Fun(commands.Cog):
    """Various fun commands and games."""

    async def _penis_awe(self, msg: discord.Message):
        await asyncio.sleep(3)
        await msg.reply('<:blop:1544849424956792932>')

    @commands.command(aliases=['pp', 'gock'])
    async def penis(self, ctx: commands.Context):
        """Generates an ASCII penis with a random length for you."""
        # TODO seed this for every user
        # TODO rotate seed every 12 hours (5:30am, 5:30pm)

        balls_chars = ['8', '0', 'Ɛ']
        shaft_chars = ['=', '≈', '≅']
        head_chars = ['D', ')', ']']


        length = randrange(2, 61)

        h = choice(head_chars)
        s = choice(shaft_chars)
        b = choice(balls_chars)

        msg = await ctx.send(b + (s * length) + h)

        if length > 7:
            asyncio.create_task(self._penis_awe(msg))


async def setup(bot: BlopBot):
    await bot.add_cog(Fun())
