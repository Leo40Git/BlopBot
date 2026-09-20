import zoneinfo
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from discord.ext import commands

ALL_TIMEZONES = frozenset(zoneinfo.available_timezones())


class TimeZoneKeyConverter(commands.Converter[str]):
    async def convert(self, ctx: commands.Context, argument: str) -> str:
        # TODO recognize more timezone names

        if argument not in ALL_TIMEZONES:
            raise BadTimeZoneKeyArgument(argument)

        return argument


class BadTimeZoneKeyArgument(commands.BadArgument):
    def __init__(self, argument: str) -> None:
        self.argument: str = argument
        super().__init__(f'"{argument}" is not a recognized time zone.')
