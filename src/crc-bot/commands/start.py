from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common.checks import get_first_name, get_id
from db import add_user, user_in_db
from menu import main_menu

router = Router()

new_user_msg: str = f"""
CRC Bot is a currency converter with built-in calculator and monitoring of exchange rates, which are updated every day via exchange-api.
\nThe converter is always active, just send a number or math expression. \
The result of the expression will be automatically calculated and converted to the final currency.
\nMenu buttons:
*Rate* — find out the exchange rate
*From/To* — set currency pair
*Round* — enable or disable rounding
*↔️* — swap currencies
\nCommands:
/start — run bot
/help — how to use
`/from USD` — set currency from
`/to EUR` — set currency to
`/pair USD EUR` — set currency pair
/swap — swap currencies
/about — info, author and contacts
"""


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    user_id = await get_id(message)
    user_name = await get_first_name(message)

    if await user_in_db(user_id):
        menu = await main_menu(user_id)
        # start message for old user
        await message.answer(
            text=f"Welcome back, {user_name}!",
            parse_mode="Markdown",
            reply_markup=menu,
        )

    else:
        menu = await main_menu(user_id, new_user=True)
        await add_user(user_id)
        # start message for new user
        await message.answer(
            text=f"Welcome, {user_name}!\n{new_user_msg}",
            parse_mode="Markdown",
            reply_markup=menu,
        )
