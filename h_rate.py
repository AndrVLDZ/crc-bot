import db
import qiwi
from tools import check_user
from aiogram import types, F, Router
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message(F.text == "Rate")
async def rate(message: types.Message) -> DeleteMessage:
    if await check_user(message):
        user_id = message.from_user.id
        rate = await qiwi.get_rate(user_id)
        if not rate: 
            await message.answer(
                "Set different currencies!",
            )
        else:
            currency_from = await db.get_from(user_id)
            currency_to = await db.get_to(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"**1 {currency_to}  ==  `{rate}` {currency_from} ",
                    parse_mode="Markdown",
                )
    # removing user input for better readability of rate responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
