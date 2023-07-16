from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common import check_user

router = Router()

help_msg: str = f"""
\nRates are updated every day and the converter is always active, just send a number or a mathematical expression. \
The result of the expression will be automatically calculated and converted to the final currency. 
\nMenu buttons:
*Rate* — exchange rate of the currency pair
*From/To* — specify your currency pair
*Round* — enable or disable rounding
*↔️* — swap currency from and currency to 
\nCommands: 
/start — run the bot
/from — set currency from [/from USD]
/to — set currency to [/to EUR]
/pair — specify your currency pair [/pair USD EUR]
/swap — swap currency from and currency to
/help — how to use the bot
/about — information about the project, author and contacts
"""


@router.message(Command(commands=["help"]))
async def about(message: Message):
    if await check_user(message):
        await message.answer(
            text=help_msg,
            parse_mode="Markdown",
        )
