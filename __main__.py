import discord
from discord.ext import commands
from dotenv import dotenv_values

config = dotenv_values(".env")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="b!", intents=intents)

bot.load_extension("cogs", recursive=True)

bot.run(config["TOKEN"])
