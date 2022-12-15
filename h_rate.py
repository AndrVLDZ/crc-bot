import db
import qiwi
from aiogram import types, F, Router
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message(F.text == "Rate")
async def rate(message: types.Message) :
    user_id = message.from_user.id
    if db.check_user(user_id):
        rate = await qiwi.get_rate(user_id)
        if bool(rate):
            currency_from = db.get_from(user_id)
            currency_to = db.get_to(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"**1 {currency_to}  ==  `{rate}` {currency_from} ",
                    parse_mode="Markdown",
                )
                return DeleteMessage(
                    chat_id=message.chat.id,
                    message_id=message.message_id)
            elif currency_from == currency_to:
                await message.answer(
                    "Currency *from* is equal to currency *to*, set different values!",
                    parse_mode="Markdown",
                )
                return DeleteMessage(
                    chat_id=message.chat.id,
                    message_id=message.message_id)
        else:
            await message.answer("Set currencies!")
            return DeleteMessage(
                chat_id=message.chat.id,
                message_id=message.message_id)
    else:
        await message.answer(
            "Send `/start` command and set currencies!", parse_mode="Markdown"
        )
        return DeleteMessage(
            chat_id=message.chat.id,
            message_id=message.message_id)
