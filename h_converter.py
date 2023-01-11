import db
import qiwi
import menu
from math import isnan, isinf
from tools import check_user
from aiogram import Router
from aiogram.types import Message
from cexprtk import evaluate_expression as evaluate

router = Router()


@router.message()
async def converter(message: Message):
    if await check_user(message):
        user_id = message.from_user.id
        main_menu = await menu.main_menu(user_id)
        # variable to store user input
        value: float = .0
        # trying to evaluate user input
        try:
            value = evaluate(
                message.text.replace(",",".").replace(" ", ""), {}
                )
            print(value, type(value))
        except:
            await message.answer(
                text="Enter a number or a valid math expression",
                reply_markup=main_menu,
            )
            return
           
        # getting user settings
        curr_from, curr_to = await db.get_currency_pair(user_id)
        # calling and validating the converter function
        if curr_from == curr_to:
            await message.answer(
                text="Set different currencies!",
                reply_markup=main_menu,
            )
            return
        
        # getting user settings
        round_res = await db.get_round_state(user_id)
        
        res = await qiwi.converter(user_id, value, round_res)
        if type(res) == float and res == 0 and round_res:
            await message.answer(
                text="Zero result after rounding",
                reply_markup=main_menu,
            )
            return
        
        if type(res) == float and res == 0 and not round_res:
            await message.answer(
                text="Zero result",
                reply_markup=main_menu,
            )
            return
        
        if isnan(res):
            await message.answer(
                text="Result is undefined",
                reply_markup=main_menu,
            )
            return
        
        if isinf(res):
            await message.answer(
                text="Cannot divide by zero",
                reply_markup=main_menu,
            )
            return
            
        if res: 
            if round_res: 
                value = round(value, 4)
            await message.answer(
                f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                parse_mode="Markdown",
                reply_markup=main_menu,
            )

