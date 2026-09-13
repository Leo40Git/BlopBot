import logging
from typing import Union

import discord
from discord.ext import commands
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase

from utils.context import Context

log = logging.getLogger('BlopBot')

initial_extensions = [
    'cogs.meta',
    'cogs.fun'
]


# noinspection unused-parameter
def _prefix_callable(bot: BlopBot, msg: discord.Message):
    return ['!', 'b!', 'B!']


class BlopBot(commands.Bot):
    bot_app_info: discord.AppInfo
    db_client: AsyncMongoClient

    def __init__(self):
        allowed_mentions = discord.AllowedMentions(roles=False, everyone=False, users=True)
        _intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            reactions=True,
            message_content=True
        )
        super().__init__(
            command_prefix=_prefix_callable,
            chunk_guilds_at_startup=False,
            allowed_mentions=allowed_mentions,
            intents=_intents
        )

    async def setup_hook(self) -> None:
        self.bot_app_info = await self.application_info()
        self.owner_id = self.bot_app_info.owner.id

        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                log.exception(
                    "Failed to load initial extension '%s'.", extension,
                    exc_info=e)

    @property
    def owner(self) -> discord.User:
        return self.bot_app_info.owner

    @property
    def db(self) -> AsyncDatabase:
        return self.db_client.get_default_database()

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('This command cannot be used in private messages.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.author.send('Sorry, this command is disabled and cannot be used.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send('I don\'t know this command...')
        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if not isinstance(original, discord.HTTPException):
                log.exception("In '%s':", ctx.command.qualified_name, exc_info=original)
        elif isinstance(error, commands.UserInputError):
            await ctx.send(str(error))

    async def get_context(
        self,
        origin: Union[discord.Message, discord.Interaction],
        /,
        *,
        cls=Context,
    ) -> Context:
        return await super().get_context(origin, cls=cls)
