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
async def converter_entry_validation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not await db.check_user(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
            )
    else:
        curr_from, curr_to = await db.get_currency_pair(user_id)
        converter_menu = await menu.converter(user_id)
        await message.answer(
            f"Enter how much currency you want to buy \
                \nBuy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
            parse_mode="Markdown",
            reply_markup=converter_menu
        )
        await state.set_state(Converting.converter_launched)


@router.message(F.text == "Round: on")
async def round_on(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    await db.set_round_state(user_id, False)
    converter_menu = await menu.converter(user_id)
    await message.answer(
        "Round off",
        reply_markup=converter_menu
        )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


@router.message(F.text == "Round: off")
async def round_off(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    await db.set_round_state(user_id, True)
    converter_menu = await menu.converter(user_id)
    await message.answer(
        "Round on",
        reply_markup=converter_menu
        )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


@router.message(F.text == "Back")
async def back(message: Message, state: FSMContext):
    main_menu = await menu.main_menu()
    await message.answer("Menu", reply_markup=main_menu)
    await state.clear()


@router.message(Converting.converter_launched)
async def converter(message: Message) -> DeleteMessage:
    # user input validation
    try:
        value = float(message.text)
    except:
        await message.answer("Enter a number, like 10 or 10.5")
        
    # getting user settings
    user_id = message.from_user.id
    round = await db.get_round_state(user_id)
    
    # calling and validating the converter function
    res = await qiwi.converter(user_id, value, round)
    if not res:
        await message.answer(
            "Set different currencies!",
            parse_mode="Markdown"
        )
    else:
        curr_from, curr_to = await db.get_currency_pair(user_id)
        if curr_from != curr_to and curr_from in qiwi.CODES and curr_to in qiwi.CODES: 
            await message.answer(
                f"**{value} {curr_to}  ==  `{res}` {curr_from}**",
                parse_mode="Markdown"
            )

    # removing user input for better readability of converter responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
