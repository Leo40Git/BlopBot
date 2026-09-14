from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from discord.ext import commands


class ZoneInfoConverter(commands.Converter[ZoneInfo]):
    async def convert(self, ctx: commands.Context, argument: str) -> ZoneInfo:
        try:
            return ZoneInfo(argument)
        except ValueError, ZoneInfoNotFoundError:
            raise BadZoneInfoArgument(argument)


class BadZoneInfoArgument(commands.BadArgument):
    def __init__(self, argument: str) -> None:
        self.argument: str = argument
        super().__init__(f'"{argument}" is not a recognized time zone.')
