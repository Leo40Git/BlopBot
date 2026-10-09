from typing import AsyncContextManager

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase

from database.entities import ScheduledEvent, UserPreferences, GuildPreferences


class Database(AsyncContextManager):
    _client: AsyncMongoClient
    mongo: AsyncDatabase

    def __init__(self, host: str):
        self._client = AsyncMongoClient(host, tz_aware=True)
        self.mongo = self._client.get_database('blopbot')

    async def migrate(self):
        # TODO. for now we'll just explicitly connect here
        await self._client.aconnect()

    async def __aexit__(self, *exc_info):
        await self._client.close()

    @property
    def guild_prefs(self) -> AsyncCollection[GuildPreferences]:
        return self.mongo['guild_prefs']

    @property
    def user_prefs(self) -> AsyncCollection[UserPreferences]:
        return self.mongo['user_prefs']

    @property
    def scheduled_events(self) -> AsyncCollection[ScheduledEvent]:
        return self.mongo['scheduled_events']
