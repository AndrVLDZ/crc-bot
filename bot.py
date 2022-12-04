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

logging.basicConfig(level=logging.INFO)

qiwi_token = tkn.get("qiwi_token.txt")
bot_token = tkn.get("bot_token.txt")

bot = Bot(token=bot_token)
dp = Dispatcher()

# connecting handlers
dp.include_router(h_start.router)
dp.include_router(h_set_currencies.router)
dp.include_router(h_rate.router)
dp.include_router(h_converter.router)
dp.include_router(h_about.router)

#  exchange rates update
async def get_rates():
    await qiwi.get_rates(qiwi_token)


#  periodic tasks for event loop
async def scheduler():
    p = Periodic(60, get_rates)
    await p.start()


async def main() -> None:
    #  create table if not exists
    db.create_table()
    # getting exchange rates
    await qiwi.get_rates(qiwi_token)
    # event loop for periodic tasks
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, loop=loop)


if __name__ == "__main__":
    asyncio.run(main())
