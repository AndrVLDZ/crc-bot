import db
import qiwi
import get_token as tkn
import h_start
import h_set_currencies
import h_rate
import h_converter
import h_about
import asyncio
from aiogram import Bot, Dispatcher
from periodic import Periodic
import logging
import os
from os import environ

logging.basicConfig(level=logging.INFO)
# TODO: if all(x in os.environ for x in["BOT_TOKEN", "QIWI_TOKEN"])
if "BOT_TOKEN" in os.environ and "QIWI_TOKEN" in os.environ:
    bot_token = environ.get("BOT_TOKEN")
    qiwi_token = environ.get("QIWI_TOKEN")
else:
    bot_token = tkn.get("bot_token.txt")
    qiwi_token = tkn.get("qiwi_token.txt")

bot = Bot(token=bot_token)
dp = Dispatcher()

# connecting handlers
dp.include_router(h_start.router)
dp.include_router(h_set_currencies.router)
dp.include_router(h_rate.router)
dp.include_router(h_converter.router)
dp.include_router(h_about.router)


# exchange rates update
async def get_rates():
    await qiwi.get_rates(qiwi_token)
    print("_____RATES_UPDATED_____")


# periodic tasks for event loop
async def scheduler():
    # exchange rates update every minute
    p = Periodic(60, get_rates)
    await p.start()


async def main() -> None:
    # create table if not exists
    await db.create_table()
    # getting exchange rates
    await qiwi.get_rates(qiwi_token)
    # event loop for periodic tasks
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, loop=loop)


if __name__ == "__main__":
    asyncio.run(main())
