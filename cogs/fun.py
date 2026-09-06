import asyncio
from random import choice, randrange

from discord.ext import commands

from bot import BlopBot


class Fun(commands.Cog):
    """Various fun commands and games."""

    @commands.command(aliases=['pp', 'gock'])
    async def penis(self, ctx: commands.Context):
        """Generates an ASCII penis with a random length for you."""
        balls_chars = ['8', 'O', 'Ɛ']
        shaft_chars = ['=', '≈', '≅']
        head_chars = ['D', ')', ']']


        length = randrange(3, 12)

        h = choice(head_chars)
        s = choice(shaft_chars)
        b = choice(balls_chars)

        await ctx.send(b + (s * length) + h)

        if length > 7:
            await asyncio.sleep(1)
            await ctx.send('<:blop:1544849424956792932>')


async def setup(bot: BlopBot):
    await bot.add_cog(Fun(bot))
