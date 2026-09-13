from typing import TYPE_CHECKING

import discord.abc
from discord.ext import commands
from pymongo.asynchronous import collection
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from utils.database import UserEntity

if TYPE_CHECKING:
    from bot import BlopBot


class Context(commands.Context):
    bot: BlopBot

    @property
    def db(self) -> AsyncDatabase:
        return self.bot.db

    async def read_user_entity(self, user: discord.User | discord.Member) -> UserEntity:
        collection: AsyncCollection[UserEntity] = self.db['users']
        result = await collection.find_one({ 'owner': user.id })
        if result is None:
            # noinspection argument-list
            result = UserEntity(owner=user.id)
            await collection.insert_one(result)
        return result

    async def update_user_entity(self, entity: UserEntity):
        collection: AsyncCollection[UserEntity] = self.db['users']
        await collection.replace_one({ 'owner': entity['owner'] }, entity)
