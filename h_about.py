from tools import check_user
from aiogram.filters import Command
from aiogram import Router, __version__
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, Message

router = Router()

msg_about: str = f""" 
**QIWI Converter Rate Calculator**
Version: 1.2
Author: Vladislav Andronov
Email: andr.vldz@gmail.com
Powered by aiogram {__version__}
"""


@router.message(Command(commands=["about"]))
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