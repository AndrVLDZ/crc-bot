import db
import menu
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# the bot will automatically calculate the value of the expression and translate the result into the final currency.

new_user_msg: str = f""" 
I have currency converter, calculator and monitoring of QIWI Wallet exchange rates.
The converter is always active after the start, just send a number or a mathematical expression. The result of the expression will be automatically converted to the final currency.
> in decimal fractions you can put a comma instead of a point, the bot will understand everything.
> And in addition, rates are updated every minute.
\nMenu buttons & commands:
`Rate` — returns the exchange rate of the currency pair
`Set currencies` — here you can specify your currency pair
`Round` — allows you to enable or disable rounding 
/about — information about the program and the author, links and ways to contact the developer
/help — how to use the bot
"""

@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if await db.check_user_id(user_id):
        main_menu = await menu.main_menu(user_id)
        curr_from, curr_to = await db.get_currency_pair(user_id)
        # start message for old user
        await message.answer(
            f"Welcome back, {user_name}! \
                \nYour last currencies settings: \
                    \nBuy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
            parse_mode="Markdown",
            reply_markup=main_menu,
        )
    else:
        main_menu = await menu.main_menu(user_id, new_user=True)
        await db.add_user(user_id)
        # start message for new user
        await message.answer(
            f"Welcome, {user_name}!\n{new_user_msg}",
            parse_mode="Markdown",
            reply_markup=main_menu,
        )

#  QIWI exchange rates are updated every minute
#  The converter is always active after the start, just send a number or a mathematical expression, the bot will automatically calculate the value of the expression and translate the result into the final currency
#  In addition, in decimal fractions, you can put a comma instead of a point, the bot will understand everything
# 
#  [Rate] — returns the exchange rate of the currency pair selected by [set currencies]
#  [Round] — allows you to enable or disable rounding for the [Rate] and converter
#  [Set currencies] — here you can specify your currency and the currency you want to buy
#  Your settings will be displayed under the currency setting buttons in the information message and there is also a currency swap button
#  /about — information about the program and the author, links and ways to contact the developer
#  /help — how to use the bot | If you do not understand how to use - send /help