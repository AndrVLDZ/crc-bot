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
        # user input
        value: str = message.text.replace(",",".")
        # user input validation
        if value == 0:
            await message.answer(
                "Enter a non-zero value!",
                reply_markup=menu.main_menu(user_id),
            )
        # getting user settings
        user_id = message.from_user.id
        round = await db.get_round_state(user_id)
        # calling and validating the converter function
        res = await qiwi.converter(user_id, value, round)
        if not res:
            await message.answer(
                "Set different currencies!",
                reply_markup=menu.main_menu(user_id),
            )
        else: 
            curr_from, curr_to = await db.get_currency_pair(user_id)
            if curr_from != curr_to: 
                await message.answer(
                    f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                    parse_mode="Markdown",
                    reply_markup=menu.main_menu(user_id),
                )
    # removing user input for better readability of converter responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
