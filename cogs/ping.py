import discord
from discord.ext import commands


class Ping(commands.Cog):
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.reply("Pong!")


def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))
