from menu import main_menu
from db import check_user_id, get_currency_pair, add_user
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

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
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if await check_user_id(user_id):
        menu = await main_menu(user_id)
        curr_from, curr_to = await get_currency_pair(user_id)
        # start message for old user
        await message.answer(
            f"Welcome back, {user_name}! \
            \nYour last currencies settings: \
            \nBuy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
            parse_mode="Markdown",
            reply_markup=menu,
        )
    else:
        menu = await main_menu(user_id, new_user=True)
        await add_user(user_id)
        # start message for new user
        await message.answer(
            f"Welcome, {user_name}!\n{new_user_msg}",
            parse_mode="Markdown",
            reply_markup=menu,
        )
