from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from common import check_user

router = Router()

help_msg: str = f"""
\nRates are updated every day via exchange-api and the converter is always active, just send a number math expression. \
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


@router.message(Command(commands=["help"]))
async def about(message: Message):
    if await check_user(message):
        await message.answer(
            text=help_msg,
            parse_mode="Markdown",
        )
