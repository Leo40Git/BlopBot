from typing import TYPE_CHECKING

from discord import User, Member
from discord.ext import commands
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from utils.database import UserSettings

if TYPE_CHECKING:
    from bot import BlopBot


class Context(commands.Context[BlopBot]):
    bot: BlopBot

    @property
    def db(self) -> AsyncDatabase:
        return self.bot.db

    async def get_user_settings(self, user: User | Member) -> UserSettings:
        c: AsyncCollection[UserSettings] = self.db['user-settings']
        result = await c.find_one({'_id': user.id})
        if result is None:
            result = UserSettings(_id=user.id)
        return result

    async def set_user_settings(self, entity: UserSettings):
        c: AsyncCollection[UserSettings] = self.db['user-settings']
        await c.replace_one(
            {'_id': entity['_id']},
            entity,
            upsert=True
        )
