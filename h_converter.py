import db
import qiwi
import menu
from typing import Union
from tools import check_user
from aiogram import Router
from aiogram.types import Message
from cexprtk import evaluate_expression as calculate

router = Router()


@router.message()
async def converter(message: Message):
    if await check_user(message):
        user_id = message.from_user.id
        # calculating of user input
        try:
            value = float(calculate(message.text.replace(",",".").replace(" ", ""), {}))
        except:
            main_menu = await menu.main_menu(user_id)
            await message.answer(
                text="Send a number or correct math expression",
                reply_markup=main_menu,
            )        
        # getting user settings
        round = await db.get_round_state(user_id)
        # calling and validating the converter function
        res = await qiwi.converter(user_id, value, round)
        if not res:
            main_menu = await menu.main_menu(user_id)
            await message.answer(
                text="Set different currencies!",
                reply_markup=main_menu,
            )
        if res: 
            main_menu = await menu.main_menu(user_id)
            curr_from, curr_to = await db.get_currency_pair(user_id)
            if curr_from != curr_to: 
                await message.answer(
                    f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                    parse_mode="Markdown",
                    reply_markup=main_menu,
                )

