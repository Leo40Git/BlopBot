import asyncio
from datetime import timezone, tzinfo, datetime, timedelta

import discord
from bson import Int64
from discord.ext import commands
from pymongo import errors

from bot import BlopBot
from utils.context import Context
from utils.database import ScheduledEvent


class Schedule(commands.Cog):
    """Commands relating to scheduling future events, such as reminders."""

    def __init__(self, bot: BlopBot):
        self.bot = bot
        self._have_new_events = asyncio.Event()
        self._current_event: ScheduledEvent | None = None
        self._dispatch_task: asyncio.Task[None] | None = None

    async def cog_load(self) -> None:
        self._dispatch_task = self.bot.loop.create_task(self._dispatch_scheduled_events())

    async def cog_unload(self) -> None:
        if self._dispatch_task is not None:
            self._dispatch_task.cancel()
            self._dispatch_task = None

    async def create_scheduled_event(
            self,
            name: str,
            triggers_at: datetime,
            *args,
            created_at: datetime | None = None,
            **kwargs
    ) -> ScheduledEvent:
        """
        Creates a new scheduled event.

        Parameters
        ----------
        name:
            The name of the event. Listen to it with 'on_{name}'.

        triggers_at:
            When the event should fire.

        *args:
            Positional arguments to pass to the event.

        created_at:
            When the event was created. Defaults to the current date and time.

        **kwargs:
            Keyword arguments to pass to the event.
        """

        created_at = created_at or discord.utils.utcnow()

        event = ScheduledEvent(
            name=name,
            created_at=created_at,
            triggers_at=triggers_at,
            args=args,
            kwargs=kwargs
        )

        delta = (triggers_at - created_at).total_seconds()
        if delta <= 60:
            # if the event is in a minute or less, don't bother adding it to the database
            self.bot.loop.create_task(self._wait_for_scheduled_event(event, seconds=delta))
            return event

        result = await self.bot.db.scheduled_events.insert_one(event)
        # noinspection typed-dict
        event['_id'] = result.inserted_id

        self._have_new_events.set()

        return event

    async def _wait_for_scheduled_event(self, event: ScheduledEvent, seconds: float):
        await asyncio.sleep(seconds)
        self.bot.dispatch(event['name'], event)

    async def _invoke_scheduled_event(self, event: ScheduledEvent):
        _id = event.get('_id')
        if _id is not None:
            # delete event from database
            await self.bot.db.scheduled_events.delete_one({'_id': _id})

        # dispatch the event!
        self.bot.dispatch(event['name'], event)

    async def _get_active_scheduled_event(self, *, days = 7) -> ScheduledEvent | None:
        return await self.bot.db.scheduled_events.find_one(
            {
                'triggers_at': {
                    '$lt': discord.utils.utcnow() + timedelta(days=days)
                }
            }
        )

    async def _wait_for_active_scheduled_events(self, *, days = 7) -> ScheduledEvent:
        event = await self._get_active_scheduled_event(days=days)
        if event is not None:
            self._have_new_events.set()
            return event

        self._have_new_events.clear()
        self._current_event = None
        await self._have_new_events.wait()

        # at this point, we always have new events
        # noinspection bad-return
        return await self._get_active_scheduled_event(days=days)

    async def _dispatch_scheduled_events(self):
        try:
            while not self.bot.is_closed():
                event = self._current_event = await self._wait_for_active_scheduled_events(days=48)
                now = discord.utils.utcnow()

                if event['triggers_at'] >= now:
                    to_sleep = (event['triggers_at'] - now).total_seconds()
                    await asyncio.sleep(to_sleep)

                await self._invoke_scheduled_event(event)
        except asyncio.CancelledError:
            raise
        except (OSError, discord.ConnectionClosed, errors.PyMongoError):
            if self._dispatch_task is not None:
                self._dispatch_task.cancel()

            self._dispatch_task = self.bot.loop.create_task(self._dispatch_scheduled_events())

    @commands.command()
    async def scheduletest(self, ctx: Context):
        tz: tzinfo = await ctx.db.get_user_timezone(ctx.author) or timezone.utc
        now = datetime.now(tz)
        in_2mins = now + timedelta(minutes=2)
        se = await self.create_scheduled_event(
            #name='test_event', created_at=now, triggers_at=in_2mins,
            #channel=Int64(ctx.channel.id)
            'test_event', in_2mins, Int64(ctx.channel.id),
            created_at=now
        )
        await ctx.send(f'what the hell, sure (`{se['_id']}`)')

    @commands.Cog.listener()
    async def on_test_event(self, event: ScheduledEvent):
        channel_id = int(event['args'][0])

        try:
            channel = self.bot.get_channel(channel_id) or (await self.bot.fetch_channel(channel_id))
            await channel.send("test event fired holy shit")
        except discord.HTTPException:
            return


async def setup(bot: BlopBot):
    await bot.add_cog(Schedule(bot))
