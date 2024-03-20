import schedule
import asyncio
from .automail import remind



schedule.every().day.at("06:00").do(lambda: asyncio.create_task(remind()))


async def jobs_run():
  while True:
    schedule.run_pending()
    await asyncio.sleep(1)
