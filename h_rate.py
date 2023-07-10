from rates import get_rate
from tools import check_user
from db import get_from, get_to
from menu import main_menu
from aiogram import F, Router
from aiogram.types import Message
from bot import bot

router = Router()


@router.message(F.text.startswith("Rate: "))
async def rate(message: Message):
    user_id = await check_user(message)
    if user_id:
        rate = await get_rate(user_id)
        if not rate: 
            await message.answer(
                "Set different currencies!",
            )
        else:
            currency_from = await get_from(user_id)
            currency_to = await get_to(user_id)
            menu = await main_menu(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"**1 {currency_from}  ==  `{rate}` {currency_to} ",
                    parse_mode="Markdown",
                    reply_markup=menu,
                )
    await bot.delete_message(message.chat.id, message.message_id)

            
