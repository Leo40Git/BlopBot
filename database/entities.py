from datetime import datetime
from typing import TypedDict, Required, ReadOnly, NotRequired, Sequence, Any, Mapping

from bson import Int64, ObjectId


class GuildPreferences(TypedDict, total=False):
    _id: Required[ReadOnly[Int64]]


class UserPreferences(TypedDict, total=False):
    _id: Required[ReadOnly[Int64]]
    tz_key: str


class ScheduledEvent(TypedDict):
    _id: NotRequired[ReadOnly[ObjectId]]
    created_at: datetime
    triggers_at: datetime
    name: str
    args: Sequence[Any]
    kwargs: Mapping[str, Any]
