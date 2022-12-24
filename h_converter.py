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


# @router.message(F.text == "Converter")
# async def converter_entry_validation(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if not await db.check_user(user_id):
#         await message.answer(
#             "Send `/start` command first!",
#             parse_mode="Markdown"
#             )
#     else:
#         curr_from, curr_to = await db.get_currency_pair(user_id)
#         converter_menu = await menu.converter(user_id)
#         await message.answer(
#             f"Enter how much currency you want to buy \
#                 \nBuy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
#             parse_mode="Markdown",
#             reply_markup=converter_menu
#         )
#         await state.set_state(Converting.converter_launched)


@router.message(F.text == "Round: on")
async def round_on(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    if not await db.check_user(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
        )
    else: 
        await db.set_round_state(user_id, False)
        main_menu = await menu.main_menu(user_id)
        await message.answer(
            "Round off",
            reply_markup=main_menu
            )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


@router.message(F.text == "Round: off")
async def round_off(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    if not await db.check_user(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
        )
    else:
        await db.set_round_state(user_id, True)
        main_menu = await menu.main_menu(user_id)
        await message.answer(
            "Round on",
            reply_markup=main_menu
            )
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )


# @router.message(F.text == "Back")
# async def back(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     if not await db.check_user(user_id):
#         await message.answer(
#             "Send `/start` command first!",
#             parse_mode="Markdown"
#         )
#     else:
#         main_menu = await menu.main_menu()
#         await message.answer("Menu", reply_markup=main_menu)
#         # await state.clear()


# def comma_replacement(expression: str):
#     return expression.replace(',','.')


@router.message()
async def converter(message: Message) -> DeleteMessage:
    user_id = message.from_user.id
    if not await db.check_user(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
            )
    else:
        # user input
        value: str = message.text.replace(',','.')
        # getting user settings
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
            if curr_from != curr_to: 
                await message.answer(
                    f"**`{value}` {curr_to}  ==  `{res}` {curr_from}**",
                    parse_mode="Markdown"
                )


    # removing user input for better readability of converter responses
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
