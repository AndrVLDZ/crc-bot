from platform import python_version
from asyncio import get_event_loop, run, sleep
from aiogram import Dispatcher

from common.logs import log
from common.bot import bot
from db import create_table
from common.rates import get_rates

from commands import start
from commands import curr_commands
from commands import help
from commands import about
from handlers import set_currencies, set_currencies
from handlers import rate, rate
from handlers import round, round
from handlers import converter, converter


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
