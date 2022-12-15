import db
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods.delete_message import DeleteMessage
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from dataclasses import dataclass


router = Router()

# all currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]

@dataclass
class Data:
    info_msg: Message = None
    swap_button: InlineKeyboardButton = None
        
        
class CurrencyCB(CallbackData, prefix="currency_callback"):
    user_id: int  # user id from [Telegram API](https://core.telegram.org/constructor/user)
    conv_prefix: str  # e.g. "To" or "From"
    currency: str  # e.g. "USD", "RUB", ...


@router.message(F.text == "Set currencies")
async def currency_pair_chooser(message: Message) -> DeleteMessage:
    def generate_buttons(pref) -> InlineKeyboardBuilder:
        builder = InlineKeyboardBuilder()
        for curr in CURRENCIES:
            cb_data = CurrencyCB(
                user_id=message.from_user.id, 
                conv_prefix=pref, 
                currency=curr
            )

            builder.add(
                InlineKeyboardButton(
                    text=curr, 
                    callback_data=cb_data.pack())
            )
        return builder

    curr_from = generate_buttons("From")
    await message.answer("I have", reply_markup=curr_from.as_markup())

    curr_to = generate_buttons("To")
    await message.answer("I want to buy", reply_markup=curr_to.as_markup())
    
    Data.swap_button = InlineKeyboardBuilder().add(InlineKeyboardButton(
            text="↔️",
            callback_data=CurrencyCB(
                user_id=message.from_user.id, 
                conv_prefix="Swap", 
                currency=""
            ).pack()
        )
    )

    user_id=message.from_user.id
    Data.info_msg = await message.answer(
        text=f"**{db.get_from(user_id)}  >>  {db.get_to(user_id)}**",
        parse_mode="Markdown",
        reply_markup=Data.swap_button.as_markup())
    
    return DeleteMessage(
        chat_id=message.chat.id,
        message_id=message.message_id)



@router.callback_query(CurrencyCB.filter())
async def save_currency(callback: CallbackQuery, callback_data: CurrencyCB) -> DeleteMessage:
    user_id = callback_data.user_id
    prefix = callback_data.conv_prefix
    currency = callback_data.currency
    if prefix == "From":
        db.set_from(user_id, currency)
    elif prefix == "To":
        db.set_to(user_id, currency)
    else:
        curr_from = db.get_from(user_id)
        curr_to = db.get_to(user_id)
        db.set_from(user_id, curr_to)
        db.set_to(user_id, curr_from)
        
    await callback.answer()
    
    edit_msg = EditMessageText(
        chat_id=callback.message.chat.id,
        message_id=Data.info_msg.message_id,
        text=f"**{db.get_from(user_id)}  >>  {db.get_to(user_id)}**",
        parse_mode="Markdown",
        reply_markup=Data.swap_button.as_markup())
    
    return edit_msg