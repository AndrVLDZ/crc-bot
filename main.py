from asyncio import get_event_loop, run, sleep
from platform import python_version

from aiogram import Dispatcher

import commands.start as start
import commands.curr_commands as curr_commands
import commands.help as help
import commands.about as about
import handlers.set_currencies as set_currencies
import handlers.rate as rate
import handlers.round as round
import handlers.converter as converter

from logs import log
from bot import bot
from db import create_table
from rates import get_rates

dp = Dispatcher()

# connecting handlers
dp.include_router(start.router)
dp.include_router(curr_commands.router)
dp.include_router(help.router)
dp.include_router(about.router)
dp.include_router(set_currencies.router)
dp.include_router(rate.router)
dp.include_router(round.router)
dp.include_router(converter.router)


# exchange rates update
async def upd_rates():
    await get_rates()
    log.info(f"RATES UPDATED")


# periodic tasks for event loop
async def scheduler():
    while True:
        try:
            await upd_rates()
        except Exception as e:
            log.error(f"Failed to update rates: {e}")
        await sleep(3600)  # exchange rates update every hour


async def main() -> None:
    if bot:
        log.info(f"Python version: {python_version()}")
        # create database and table if not exists
        await create_table()
        # getting exchange rates
        await get_rates()
        loop = get_event_loop()
        loop.create_task(scheduler())
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == "__main__":
    run(main())
