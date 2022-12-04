import aiogram
from aiogram import types, F, Router
from aiogram.filters.text import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()

msg_about: str = f""" 
**QIWI Exchange Bot**
Version: 1.0
Author: Vladislav Andronov
Email: andr.vldz@gmail.com
Powered by aiogram {aiogram.__version__}
"""


@router.message(F.text == "About")
async def about(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="Telegram", 
        url="https://t.me/Cepesh")
    )
    builder.row(types.InlineKeyboardButton(
        text="GitHub", 
        url="https://github.com/AndrVLDZ")
    )
    await message.answer(
        msg_about,
        parse_mode="Markdown",
        reply_markup=builder.as_markup(),
    )


@router.callback_query(Text(text="guide"))
async def guide(callback: types.CallbackQuery):
    await callback.message.answer("Guide for user [in develop]")
    await callback.answer()
