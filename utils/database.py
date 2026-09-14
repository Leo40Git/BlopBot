from typing import TypedDict, Required, ReadOnly

from discord import User, Member
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.database import AsyncDatabase


class DatabaseHelper:
    db: AsyncDatabase

    def __init__(
            self,
            client: AsyncMongoClient
    ):
        self.db = client.get_default_database()

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


class UserSettings(TypedDict, total=False):
    _id: Required[ReadOnly[int]]
    tz_key: str
