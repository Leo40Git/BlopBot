from typing import TypedDict, ReadOnly, Required, AsyncContextManager

import discord
from bson import Int64
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase


class Database(AsyncContextManager):
    _client: AsyncMongoClient
    mongo: AsyncDatabase

    def __init__(self, host: str):
        self._client = AsyncMongoClient(host)
        self.mongo = self._client.get_database('blopbot')

    async def migrate(self):
        # TODO. for now we'll just explicitly connect here
        await self._client.aconnect()

    async def __aexit__(self, *exc_info):
        await self._client.close()

    async def get_user_settings(self, user: discord.User | discord.Member) -> UserSettings:
        c: AsyncCollection[UserSettings] = self.mongo['user-settings']
        result = await c.find_one({'_id': user.id})
        if result is None:
            result = UserSettings(_id=Int64(user.id))
        return result

    async def save_user_settings(self, entity: UserSettings):
        c: AsyncCollection[UserSettings] = self.mongo['user-settings']
        await c.replace_one(
            {'_id': entity['_id']},
            entity,
            upsert=True
        )


class UserSettings(TypedDict, total=False):
    _id: Required[ReadOnly[Int64]]
    tz_key: str
