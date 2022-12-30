from tools import check_user
from aiogram import F, Router, __version__
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, Message

router = Router()

msg_about: str = f""" 
**QIWI Converter Rate Calculator**
Version: 1.1
Author: Vladislav Andronov
Email: andr.vldz@gmail.com
Powered by aiogram {__version__}
"""


@router.message(F.text == "About")
async def about(message: Message):
    if await check_user(message):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(
            text="Telegram", 
            url="https://t.me/andrvldz")
        )
        builder.row(InlineKeyboardButton(
            text="GitHub", 
            url="https://github.com/AndrVLDZ")
        )
        await message.answer(
            msg_about,
            parse_mode="Markdown",
            reply_markup=builder.as_markup(),
        )