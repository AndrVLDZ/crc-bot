from asyncio import get_event_loop, run, sleep
from platform import python_version

from aiogram import Dispatcher

import h_about
import h_converter
import h_help
import h_rate
import h_round
import h_set_currencies
import h_start
from db import create_table
from get_tokens import get_secrets
from logs import log
from rates import get_rates
from bot import bot

dp = Dispatcher()

# connecting handlers
dp.include_router(h_start.router)
dp.include_router(h_help.router)
dp.include_router(h_about.router)
dp.include_router(h_set_currencies.router)
dp.include_router(h_rate.router)
dp.include_router(h_round.router)
dp.include_router(h_converter.router)


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
    log.info(f"Python version: {python_version()}")
    # create database and table if not exists
    await create_table()
    # getting exchange rates
    await get_rates()
    loop = get_event_loop()
    loop.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, loop=loop) 


if __name__ == "__main__":
    run(main())
