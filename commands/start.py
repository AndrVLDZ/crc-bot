from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common import get_first_name, get_id
from db import add_user, get_currency_pair, user_in_db
from menu import main_menu

router = Router()

new_user_msg: str = f""" 
I have currency converter with a built-in calculator and monitoring of QIWI Wallet exchange rates that are updated every minute.
\nThe converter is always active, just send a number or a mathematical expression. \
The result of the expression will be automatically calculated and converted to the final currency.
\nMenu buttons:
*Rate* — returns the exchange rate of the currency pair
*Set currencies* — here you can specify your currency pair
*Round* — allows you to enable or disable rounding
\nCommands: 
/start — run the bot
/help — how to use the bot
/about — information about the project, author and contacts
\n*If Set currencies doesn't work* — call it again by pressing the corresponding menu button or restart the bot. \
This issue can happen if the bot has been restarted on the server or the message cannot be edited because it's too old.
"""


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    user_id = await get_id(message)
    user_name = await get_first_name(message)

    if await user_in_db(user_id):
        menu = await main_menu(user_id)
        curr_from, curr_to = await get_currency_pair(user_id)
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
