import db
import menu
from tools import check_user
from aiogram import F, Router
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage

router = Router()


@router.message(F.text == "Round: on")
async def round_on(message: Message) -> DeleteMessage:
    if await check_user(message):
        user_id = message.from_user.id
        await db.set_round_state(user_id, False)
        main_menu = await menu.main_menu(user_id)
        await message.answer(
            "Round off",
            reply_markup=main_menu
            )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


@router.message(F.text == "Round: off")
async def round_off(message: Message) -> DeleteMessage:
    if await check_user(message):
        user_id = message.from_user.id
        await db.set_round_state(user_id, True)
        main_menu = await menu.main_menu(user_id)
        await message.answer(
            "Round on",
            reply_markup=main_menu
            )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )

