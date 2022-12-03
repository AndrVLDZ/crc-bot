import db
import qiwi
from aiogram import types, F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


router = Router()

# All currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]


class CurrencyCB(CallbackData, prefix="currency_callback"):
    user_id: int  # user id from [Telegram API](https://core.telegram.org/constructor/user)
    conv_prefix: str  # e.g. "TO" or "FROM"
    currency: str  # e.g. "USD", "RUB", ...


@router.message(F.text == "Set currencies")
async def currency_pair_chooser(message: types.Message):
    def add_buttons(builder: InlineKeyboardBuilder, pref):
        for curr in CURRENCIES:
            cb_data = CurrencyCB(
                user_id=message.from_user.id, conv_prefix=pref, currency=curr
            )

            builder.add(
                types.InlineKeyboardButton(text=curr, callback_data=cb_data.pack())
            )

    curr_from = InlineKeyboardBuilder()
    add_buttons(curr_from, pref="from")
    await message.answer("I have", reply_markup=curr_from.as_markup())

    curr_to = InlineKeyboardBuilder()
    add_buttons(curr_to, pref="to")
    await message.answer("I want to buy", reply_markup=curr_to.as_markup())


async def save_currency(callback: types.CallbackQuery, data: CurrencyCB):
    curr_code = qiwi.CODES[data.currency]
    if data.conv_prefix == "from":
        db.set_from(data.user_id, curr_code)
    else:
        db.set_to(data.user_id, curr_code)

    await callback.message.answer(
        f"Currency {data.conv_prefix} has been set to {data.currency}"
    )
    await callback.answer()


@router.callback_query(CurrencyCB.filter())
async def from_usd(callback: types.CallbackQuery, callback_data: CurrencyCB):
    await save_currency(callback, callback_data)
