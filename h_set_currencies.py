import db
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery

router = Router()

# all currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]


class CurrencyCB(CallbackData, prefix="currency_callback"):
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From" 
    currency: str  # e.g. "USD", "RUB", ...


def generate_buttons(user_id: int, pref: str) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for curr in CURRENCIES:
        cb_data = CurrencyCB(
            user_id=user_id,
            conv_prefix=pref,
            currency=curr,
        )
        builder.add(
            InlineKeyboardButton(
                text=curr, 
                callback_data=cb_data.pack()
                )
        )
    return builder


async def generate_info_msg(user_id: int, message: Message, state: FSMContext):
    swap_button = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="↔️",
            callback_data=CurrencyCB(
                user_id=user_id,
                conv_prefix="Swap",
                currency="",
            ).pack(),
        )
    )
    
    curr_from, curr_to = await db.get_currency_pair(user_id)
    info_msg = await message.answer(
        text=f"Buy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
        parse_mode="Markdown",
        reply_markup=swap_button.as_markup()
    )
    
    user_data = {
        "chat_id": info_msg.chat.id,
        "message_id": info_msg.message_id,
        "swap_button": swap_button,
    }
    
    await state.set_data(user_data)


@router.message(F.text == "Set currencies")
async def currency_pair_chooser(message: Message):
    user_id=message.from_user.id
    if not await db.check_user_id(user_id):
        await message.answer(
            "Send `/start` command first!",
            parse_mode="Markdown"
        )
    else:
        curr_from = generate_buttons(user_id, "From")
        await message.answer("I have", reply_markup=curr_from.as_markup())

        curr_to = generate_buttons(user_id, "To")
        await message.answer("I want to buy", reply_markup=curr_to.as_markup())
        
        generate_info_msg(user_id, message)
        

@router.callback_query(CurrencyCB.filter())
async def save_currency(callback: CallbackQuery, callback_data: CurrencyCB, state: FSMContext):
    # getting data from callback_data
    user_id = callback_data.user_id
    prefix = callback_data.conv_prefix
    currency = callback_data.currency
    
    if prefix == "From":
        await db.set_from(user_id, currency)
    if prefix == "To":
        await db.set_to(user_id, currency)
    if prefix == 'Swap':
        curr_from, curr_to = await db.get_currency_pair(user_id)
        await db.set_currency_pair(user_id, curr_to, curr_from)
        
    await callback.answer()
    
    user_data = await state.get_data()
    curr_from, curr_to = await db.get_currency_pair(user_id)
    
    return EditMessageText(
        chat_id=user_data["chat_id"],
        message_id=user_data["message_id"],
        text=f"Buy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
        parse_mode="Markdown",
        reply_markup=user_data["swap_button"].as_markup(),
    )
