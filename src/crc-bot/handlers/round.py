from aiogram import F, Router
from aiogram.types import Message

from common.checks import check_user
from common.bot import bot
from db import set_round_state
from menu import main_menu

router = Router()


@router.message(F.text == "Round: on")
async def round_on(message: Message):
    user_id = await check_user(message)
    if user_id:
        await set_round_state(user_id, False)
        menu = await main_menu(user_id)
        await message.answer("Round off", reply_markup=menu)
    await bot.delete_message(message.chat.id, message.message_id)


@router.message(F.text == "Round: off")
async def round_off(message: Message):
    user_id = await check_user(message)
    if user_id:
        await set_round_state(user_id, True)
        menu = await main_menu(user_id)
        await message.answer("Round on", reply_markup=menu)
    await bot.delete_message(message.chat.id, message.message_id)
