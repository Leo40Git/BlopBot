from typing import TypedDict, Required, ReadOnly


class UserSettings(TypedDict, total=False):
    _id: Required[ReadOnly[int]]
    tz_key: str
