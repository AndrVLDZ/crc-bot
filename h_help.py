from tools import check_user
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

help_msg: str = f"""
\nRates are updated every minute and the converter is always active, just send a number or a mathematical expression. \
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


@router.message(Command(commands=["help"]))
async def about(message: Message):
    if await check_user(message):
        await message.answer(
            text=help_msg,
            parse_mode="Markdown",
        )