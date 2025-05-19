import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from scraping import get_fixture
import time

async def compose_message():
    date, opponent, pitch = await get_fixture()
    print(f"scheduled message: {date}, {opponent}, {pitch}")

async def schedule_message():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(compose_message, "cron", day_of_week="mon", hour=19, minute=7)
    scheduler.start()
    while True:
        await asyncio.sleep(60)

asyncio.run(schedule_message())