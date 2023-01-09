import db
import qiwi
import menu
from tools import check_user
from aiogram import Router
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message()
async def converter(message: Message) -> DeleteMessage:
    if await check_user(message):
        user_id = message.from_user.id
        # user input
        value: str = message.text.replace(",",".").replace(" ", "")
        # getting user settings
        round = await db.get_round_state(user_id)
        # calling and validating the converter function
        res = await qiwi.converter(user_id, value, round)
        if type(res) == str:
            main_menu = await menu.main_menu(user_id)
            await message.answer(
                text=res,
                reply_markup=main_menu,
            )
        if type(res) == float: 
            main_menu = await menu.main_menu(user_id)
            curr_from, curr_to = await db.get_currency_pair(user_id)
            if curr_from != curr_to: 
                await message.answer(
                    f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                    parse_mode="Markdown",
                    reply_markup=main_menu,
                )
    # removing user input for better readability of converter responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
