import db
import qiwi
from aiogram import types, F, Router
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message(F.text == "Rate")
async def rate(message: types.Message) -> DeleteMessage:
    user_id = message.from_user.id
    if not db.check_user(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
        )
    else:
        rate = await qiwi.get_rate(user_id)
        if not rate: 
            await message.answer(
                "Set different currencies!",
            )
        else:
            currency_from = db.get_from(user_id)
            currency_to = db.get_to(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"**1 {currency_to}  ==  `{rate}` {currency_from} ",
                    parse_mode="Markdown",
                )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
