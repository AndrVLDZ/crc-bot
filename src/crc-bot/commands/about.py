from aiogram import Router, __version__
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.checks import check_user

router = Router()

msg_about: str = f"""
<b>CRC Bot: Converter Rate Calculator</b>
Version: 1.3
Author: <a href="https://t.me/andrvldz">Vladislav Andronov</a>
QA: <a href="https://t.me/Tr1gun">Andrew Tr1gun</a>
Email: andr.vldz@gmail.com
Powered by aiogram {__version__}
"""


@router.message(Command(commands=["about"]))
async def about(message: Message):
    if await check_user(message):
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(
            text="GitHub Repo",
            url="https://github.com/AndrVLDZ/crc-bot")
        )
        await message.answer(
            msg_about,
            parse_mode="HTML",
            reply_markup=builder.as_markup(),
        )