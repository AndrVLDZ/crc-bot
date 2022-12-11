import db
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery


router = Router()

# All currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]


class CurrencyCB(CallbackData, prefix="currency_callback"):
    user_id: int  # user id from [Telegram API](https://core.telegram.org/constructor/user)
    conv_prefix: str  # e.g. "To" or "From"
    currency: str  # e.g. "USD", "RUB", ...


@router.message(F.text == "Set currencies")
async def currency_pair_chooser(message: Message):
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


@router.callback_query(CurrencyCB.filter())
async def save_currency(callback: CallbackQuery, callback_data: CurrencyCB):
    if callback_data.conv_prefix == "From":
        db.set_from(callback_data.user_id, callback_data.currency)
    else:
        db.set_to(callback_data.user_id, callback_data.currency)

    await callback.message.answer(
        f"{callback_data.conv_prefix}: **{callback_data.currency}**",
        parse_mode="Markdown"
    )
    await callback.answer()
