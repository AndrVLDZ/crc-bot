import db
import qiwi
import menu
from aiogram import F, Router
from aiogram.methods.delete_message import DeleteMessage
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
                    reply_markup=menu.converter(user_id),
                )
                await state.set_state(Converting.converter_launched)
            else:
                await message.answer(
                    """
                    Currency *from* is equal to currency *to*, set different values!""",
                    parse_mode="Markdown",
                )
        else:
            await message.answer(
                    """
                    Currency *from* is equal to currency *to*, set different values!""",
                    parse_mode="Markdown",
                )
            await message.answer("Set currencies!")
    else:
        await message.answer(
            """
            Send `/start` command and set currencies!""",
            parse_mode="Markdown",
        )
        
@router.message(F.text == "Round: on")
async def round_on(message: Message):
    user_id = message.from_user.id
    db.set_round(user_id, False)
    await message.answer("Round off", reply_markup=menu.converter(user_id))


@router.message(F.text == "Round: off")
async def round_off(message: Message):
    user_id = message.from_user.id
    db.set_round(user_id, True)
    await message.answer("Round on", reply_markup=menu.converter(user_id))

@router.message(F.text == "↔️")
async def round_off(message: Message):
    user_id = message.from_user.id
    curr_from = db.get_from(user_id)
    curr_to = db.get_to(user_id)
    db.set_from(user_id, curr_to)
    db.set_to(user_id, curr_from)
    currency_from = curr_to
    currency_to = curr_from
    await message.answer(f"""
                From: **{currency_from}**\nTo: **{currency_to}**""",
                parse_mode="Markdown",
                reply_markup=menu.converter(user_id),
                )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)


@router.message(F.text == "Back")
async def back(message: Message, state: FSMContext):
    await message.answer("Back to menu", reply_markup=menu.main_menu())
    await state.clear()


@router.message(Converting.converter_launched)
async def converter(message: Message, state: FSMContext):
    # user input validation
    try:
        value = float(message.text)
    except:
        await message.answer("Enter a number, lke 10 or 10.5")
    user_id = message.from_user.id
    round = db.get_round(user_id)
    print(round)
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
    await message.answer(
        "Enter another value", 
        reply_markup = menu.converter(user_id)
        )
