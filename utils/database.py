from datetime import datetime
from typing import TypedDict, ReadOnly, Required, AsyncContextManager, Mapping, Any, NotRequired, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import discord
from bson import Int64, ObjectId
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
        _id = Int64(user.id)
        c: AsyncCollection[UserSettings] = self.mongo['user_settings']
        result = await c.find_one({'_id': _id})
        if result is None:
            result = UserSettings(_id=_id)
        return result

    async def get_user_timezone(self, user: discord.User | discord.Member) -> ZoneInfo | None:
        settings = await self.get_user_settings(user)
        tz_key = settings.get('tz_key')

        tz: ZoneInfo | None = None
        try:
            if tz_key is not None:
                tz = ZoneInfo(tz_key)
        except ZoneInfoNotFoundError:
            pass

        return tz

    async def save_user_settings(self, entity: UserSettings):
        c: AsyncCollection[UserSettings] = self.mongo['user_settings']
        await c.replace_one(
            {'_id': entity['_id']},
            entity,
            upsert=True
        )

    @property
    def scheduled_events(self) -> AsyncCollection[ScheduledEvent]:
        return self.mongo['scheduled_events']


class UserSettings(TypedDict, total=False):
    _id: Required[ReadOnly[Int64]]
    tz_key: str


class ScheduledEvent(TypedDict):
    _id: NotRequired[ReadOnly[ObjectId]]
    created_at: datetime
    triggers_at: datetime
    name: str
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
