import asyncio
from random import Random, choice, randrange, getrandbits

import discord
from discord.ext import tasks, commands

from bot import BlopBot
from utils.context import Context


class Fun(commands.Cog):
    """Various fun commands and games."""

    _penis_seed: int

    def __init__(self):
        self._penis_seed = getrandbits(32)

    @commands.command(aliases=['pp', 'gock'])
    async def penis(self, ctx: Context):
        """Generates an ASCII penis with a random length for you."""

        balls_chars = ['8', '0', 'Ɛ']
        shaft_chars = ['=', '≈', '≅']
        head_chars = ['D', ')', ']']

        rng = Random(hash((ctx.author.id, self._penis_seed)))

        length = rng.randrange(2, 61)

        h = rng.choice(head_chars)
        s = rng.choice(shaft_chars)
        b = rng.choice(balls_chars)

        msg = await ctx.send(b + (s * length) + h)

        if length > 7:
            asyncio.create_task(self._penis_awe(msg))

    async def _penis_awe(self, msg: discord.Message):
        await asyncio.sleep(3)

        if msg.channel.last_message_id == msg.id:
            await msg.channel.send('<:blop:1544849424956792932>')
        else:
            await msg.reply('<:blop:1544849424956792932>')

    @tasks.loop(hours=12)
    async def _rotate_penis_seed(self):
        self._penis_seed = getrandbits(32)


async def setup(bot: BlopBot):
    await bot.add_cog(Fun())
