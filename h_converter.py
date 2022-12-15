import db
import qiwi
import menu
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods.delete_message import DeleteMessage
router = Router()


class Converting(StatesGroup):
    converter_launched = State()


@router.message(F.text == "Converter")
async def converter_pressed(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(round=True)
    if db.check_user(user_id):
        if await qiwi.get_rate(user_id):
            curr_from = db.get_from(user_id)
            curr_to = db.get_to(user_id)
            await message.answer(f"Enter how much currency you want to buy")
            if curr_from != curr_to:
                await message.answer(
                    text=f"**{curr_from}  >>  {curr_to}**",
                    parse_mode="Markdown",
                    reply_markup=menu.converter(user_id),
                )
                await state.set_state(Converting.converter_launched)
                return DeleteMessage(
                    chat_id=message.chat.id,
                    message_id=message.message_id)
            else:
                await message.answer(
                    """
                    Currency *from* is equal to currency *to*, set different values!""",
                    parse_mode="Markdown",
                )
                return DeleteMessage(
                    chat_id=message.chat.id,
                    message_id=message.message_id)

        else:
            await message.answer(
                    """
                    Currency *from* is equal to currency *to*, set different values!""",
                    parse_mode="Markdown",
                )
            await message.answer("Set currencies!")
            return DeleteMessage(
                chat_id=message.chat.id,
                message_id=message.message_id)

    else:
        await message.answer(
            """
            Send `/start` command and set currencies!""",
            parse_mode="Markdown",
        )
        return DeleteMessage(
            chat_id=message.chat.id,
            message_id=message.message_id)

        
@router.message(F.text == "Round: on")
async def round_on(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    db.set_round_state(user_id, False)
    await message.answer("Round off", reply_markup=menu.converter(user_id))
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)


@router.message(F.text == "Round: off")
async def round_off(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    db.set_round_state(user_id, True)
    await message.answer("Round on", reply_markup=menu.converter(user_id))
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)
    

@router.message(F.text == "Back")
async def back(message: Message, state: FSMContext):
    await message.answer("Menu", reply_markup=menu.main_menu())
    await state.clear()
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)


@router.message(Converting.converter_launched)
async def converter(message: Message) -> DeleteMessage:
    # user input validation
    try:
        value = float(message.text)
    except:
        await message.answer("Enter a number, like 10 or 10.5")
        return DeleteMessage(
            chat_id=message.chat.id,
            message_id=message.message_id)

    user_id = message.from_user.id
    round = db.get_round_state(user_id)
    # conversion
    res = await qiwi.converter(user_id, value, round)
    await message.answer(
        f"""
        **{value} {db.get_to(user_id)}  ==  `{res}` {db.get_from(user_id)}**""",
        parse_mode="Markdown"
    )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)
