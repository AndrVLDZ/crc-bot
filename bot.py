from asyncio import get_event_loop, run
from platform import python_version

from aiogram import Bot, Dispatcher
from periodic import Periodic

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
from qiwi import get_rates

bot_token, qiwi_token = get_secrets()

bot = Bot(token=bot_token)
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
    await get_rates(qiwi_token)
    log.info(f"RATES UPDATED")


# periodic tasks for event loop
async def scheduler():
    # exchange rates update every minute
    p = Periodic(60, upd_rates)
    await p.start()


async def main() -> None:
    log.info(f"Python version: {python_version()}")
    # create table if not exists
    await create_table()
    # getting exchange rates
    await get_rates(qiwi_token)
    loop = get_event_loop()
    loop.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, loop=loop) 


if __name__ == "__main__":
    run(main())
