import db
import qiwi
import menu
from math import isnan, isinf
from tools import check_user
from typing import Union
from aiogram import Router
from aiogram.types import Message
from cexprtk import evaluate_expression as evaluate

router = Router()


async def evaluate_value(message: Message) -> float:
    try:
        res = evaluate(
            message.text.replace(",",".").replace(" ", ""), {}
            )
        return float(res)
    except:
        main_menu = await menu.main_menu(message.from_user.id)
        await message.answer(
            text="Enter a number or a valid math expression",
            reply_markup=main_menu,
        )


async def validate_evaluated_value(message: Message, value: float) -> bool:
    user_id = message.from_user.id
    main_menu = await menu.main_menu(user_id)
    if isnan(value):
        await message.answer(
            text="Result is undefined",
            reply_markup=main_menu,
        )
        return False
    
    if isinf(value):
        await message.answer(
            text="Cannot divide by zero",
            reply_markup=main_menu,
        )
        return False
    
    return True


async def convert_value(message: Message, value: float, round_res: bool) -> Union[str, float]:
    rate = await qiwi.get_rate(message.from_user.id, converter=True)
    if not rate:
        return "Set different currencies!"
    
    res = value*rate
    if round_res:
        rounded_res = round(res, 2)
        if res != 0 and rounded_res == 0:
            return "Zero value received after rounding"
        return rounded_res
    
    return res


@router.message()
async def converting(message: Message):
    if await check_user(message):
        user_id = message.from_user.id
        value = await evaluate_value(message)
        if not await validate_evaluated_value(message, value):
            return            
    
        round_res = await db.get_round_state(user_id)
        main_menu = await menu.main_menu(user_id) 
        res = await convert_value(message, value, round_res)
        if type(res) == str:
            await message.answer(
                text=res,
                reply_markup=main_menu,
            )
            return
        
        curr_from, curr_to = await db.get_currency_pair(user_id)
        await message.answer(
            f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
            parse_mode="Markdown",
            reply_markup=main_menu,
        )
