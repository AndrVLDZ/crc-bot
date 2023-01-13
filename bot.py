import h_start
import h_rate
import h_round
import h_about
import h_help
import h_converter
import h_set_currencies
from qiwi import get_rates
from db import create_table
from get_tokens import get_secrets
import logging
from asyncio import get_event_loop, run
from periodic import Periodic
from aiogram import Bot, Dispatcher

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

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
    logging.info(f"RATES UPDATED")


# periodic tasks for event loop
async def scheduler():
    # exchange rates update every minute
    p = Periodic(60, upd_rates)
    await p.start()


async def main() -> None:
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
