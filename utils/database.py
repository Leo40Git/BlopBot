from typing import TypedDict

from discord.abc import Snowflake


class UserEntity(TypedDict):
    owner: Snowflake
    tz_key: str | None
