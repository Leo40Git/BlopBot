from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import discord
from bson import Int64
from discord.ext import commands

from bot import BlopBot
from database import UserPreferences, GuildPreferences


class Prefs(commands.Cog):
    """Preference management for guilds and users."""
    
    def __init__(self, bot: BlopBot):
        self.bot = bot
        
    async def get_guild_prefs(self, guild: discord.Guild) -> GuildPreferences:
        _id = Int64(guild.id)
        result = await self.bot.db.guild_prefs.find_one({'_id': _id})
        if result is None:
            result = GuildPreferences(_id=_id)
        return result
    
    async def save_guild_prefs(self, prefs: GuildPreferences):
        await self.bot.db.guild_prefs.replace_one(
            {'_id': prefs['_id']},
            prefs,
            upsert=True
        )
    
    async def get_user_prefs(self, user: discord.User | discord.Member) -> UserPreferences:
        _id = Int64(user.id)
        result = await self.bot.db.user_prefs.find_one({'_id': _id})
        if result is None:
            result = UserPreferences(_id=_id)
        return result

    async def get_user_timezone(self, user: discord.User | discord.Member) -> ZoneInfo | None:
        settings = await self.get_user_prefs(user)
        tz_key = settings.get('tz_key')

        tz: ZoneInfo | None = None
        try:
            if tz_key is not None:
                tz = ZoneInfo(tz_key)
        except ZoneInfoNotFoundError:
            pass

        return tz
    
    async def save_user_prefs(self, prefs: UserPreferences):
        await self.bot.db.user_prefs.replace_one(
            {'_id': prefs['_id']},
            prefs,
            upsert=True
        )


async def setup(bot: BlopBot):
    await bot.add_cog(Prefs(bot))
