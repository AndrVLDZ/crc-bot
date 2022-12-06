import db
import qiwi
import menu
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()


class Converting(StatesGroup):
    converter_launched = State()


@router.message(F.text == "Converter")
async def converter_pressed(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(round=True)
    if db.check_user(user_id):
        if await qiwi.get_rate(user_id):
            currency_from = db.get_from(user_id)
            currency_to = db.get_to(user_id)
            if currency_from != currency_to:
                await message.answer(
                    f"""
                How much {currency_to} do you want to by for {currency_from}?""",
                    parse_mode="Markdown",
                    reply_markup=menu.converter_round_on,
                )
                await state.set_state(Converting.converter_launched)
            else:
                await message.answer(
                    """
                    Currency *from* is equal to currency *to*, set different values!""",
                    parse_mode="Markdown",
                )
        else:
            await message.answer("Set currencies!")
    else:
        await message.answer(
            """
            Send `/start` command and set currencies!""",
            parse_mode="Markdown",
        )


@router.message(F.text == "Round: on")
async def round_on(message: Message, state: FSMContext):
    await state.update_data(round=False)
    await message.answer("Round off", reply_markup=menu.converter_round_off)


@router.message(F.text == "Round: off")
async def round_off(message: Message, state: FSMContext):
    await state.update_data(round=True)
    await message.answer("Round on", reply_markup=menu.converter_round_on)


@router.message(F.text == "Back")
async def back(message: Message, state: FSMContext):
    await message.answer("Back to menu", reply_markup=menu.main_menu)
    await state.clear()


@router.message(Converting.converter_launched)
async def converter(message: Message, state: FSMContext):
    # user input validation
    try:
        value = float(message.text)
    except:
        await message.answer("Enter a number, lke 10 or 10.5")
    user_id = message.from_user.id
    user_data = await state.get_data()
    round = user_data["round"]
    # conversion
    res = await qiwi.converter(user_id, value, round)
    currency_from = db.get_from(user_id)
    currency_to = db.get_to(user_id)
    await message.answer(
        f"""
        For {value} {currency_to} you will pay `{res}` {currency_from}""",
        parse_mode="Markdown",
    )
    # call menu buttons depending on rounding state
    if round:
        await message.answer(
            "Enter another value", reply_markup=menu.converter_round_on
        )
    else:
        await message.answer(
            "Enter another value", reply_markup=menu.converter_round_off
        )
