from aiogram import F, Router, __version__
from aiogram.filters.text import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message

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


@router.callback_query(Text(text="guide"))
async def guide(callback: CallbackQuery):
    await callback.message.answer("Guide for user [in develop]")
    await callback.answer()
