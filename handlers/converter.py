from math import isinf, isnan
from typing import Union

from aiogram import Router
from aiogram.types import Message
from cexprtk import evaluate_expression as evaluate

from common import check_user
from db import get_currency_pair, get_round_state
from menu import main_menu
from rates import get_rate

router = Router()


async def evaluate_value(user_id: int, message: Message) -> Union[float, bool]:
    if isinstance(message.text, str):
        try:
            res = evaluate(
                message.text.replace(",", ".").replace(" ", ""),
                {},
            )
            return float(res)
        except:
            menu = await main_menu(user_id)
            await message.answer(
                text="Enter a number or a valid math expression",
                reply_markup=menu,
            )
            return False
    return False


async def validate_evaluated_value(
    user_id: int, message: Message, value: float
) -> bool:
    if isnan(value):
        menu = await main_menu(user_id)
        await message.answer(
            text="Result is undefined",
            reply_markup=menu,
        )
        return False

    if isinf(value):
        menu = await main_menu(user_id)
        await message.answer(
            text="Cannot divide by zero",
            reply_markup=menu,
        )
        return False
    return True


async def convert_value(
    user_id: int, value: float, round_res: bool, message: Message
) -> Union[bool, float]:
    rate = await get_rate(user_id, converter=True)
    if not rate:
        menu = await main_menu(user_id)
        await message.answer(
            text="Set different currencies!",
            reply_markup=menu,
        )
        return False

    res: float = value * rate
    if round_res:
        rounded_res = round(res, 2)
        if res != 0 and rounded_res == 0:
            menu = await main_menu(user_id)
            await message.answer(
                text="Zero value received after rounding",
                reply_markup=menu,
            )
            return False
        return rounded_res
    return res


async def converter_answer(user_id: int, value: float, res: float, message: Message):
    curr_from, curr_to = await get_currency_pair(user_id)
    menu = await main_menu(user_id)
    await message.answer(
        f"**`{value}` {curr_from}  ==  `{res}` {curr_to}**",
        parse_mode="Markdown",
        reply_markup=menu,
    )


@router.message()
async def converting(message: Message):
    user_id = await check_user(message)
    if user_id:
        value = await evaluate_value(user_id, message)
        if value is not False:
            if not await validate_evaluated_value(user_id, message, value):
                return
            round_res = await get_round_state(user_id)
            res = await convert_value(user_id, value, round_res, message)
            if res is not False:
                if round_res:
                    value = round(value, 2)
                await converter_answer(user_id, value, res, message)
