import db
import qiwi
from aiogram import types, F, Router
from aiogram.filters.text import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass, field


@dataclass
class Data:
    user_id: int = field(default=0)


router = Router()

# All currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]


@router.message(F.text == "Set currencies")
async def set_currency_from(message: types.Message):
    Data.user_id = message.from_user.id

    def add_buttons(builder: InlineKeyboardBuilder, data_prefix):
        for curr in CURRENCIES:
            builder.add(
                types.InlineKeyboardButton(
                    text=curr, callback_data=f"{data_prefix}_{curr}"
                )
            )

    curr_from = InlineKeyboardBuilder()
    add_buttons(curr_from, data_prefix="from")
    await message.answer("I have", reply_markup=curr_from.as_markup())

    curr_to = InlineKeyboardBuilder()
    add_buttons(curr_to, data_prefix="to")
    await message.answer("I want to buy", reply_markup=curr_to.as_markup())

@router.callback_query(Text(text = 'from_USD'))
async def from_usd(callback: types.CallbackQuery):
    code = qiwi.codes['USD']
    db.set_from(Data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'from_EUR'))
async def from_eur(callback: types.CallbackQuery):
    code = qiwi.codes['EUR']
    db.set_from(Data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'from_RUB'))
async def from_rub(callback: types.CallbackQuery):
    code = qiwi.codes['RUB']
    db.set_from(Data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'from_KZT'))
async def from_kzt(callback: types.CallbackQuery):
    code = qiwi.codes['KZT']
    db.set_from(Data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'from_CNY'))
async def from_cny(callback: types.CallbackQuery):
    code = qiwi.codes['CNY']
    db.set_from(Data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'to_USD'))
async def to_usd(callback: types.CallbackQuery):
    code = qiwi.codes['USD']
    db.set_to(Data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'to_EUR'))
async def to_eur(callback: types.CallbackQuery):
    code = qiwi.codes['EUR']
    db.set_to(Data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'to_RUB'))
async def to_rub(callback: types.CallbackQuery):
    code = qiwi.codes['RUB']
    db.set_to(Data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'to_KZT'))
async def to_kzt(callback: types.CallbackQuery):
    code = qiwi.codes['KZT']
    db.set_to(Data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(Text(text = 'to_CNY'))
async def to_cny(callback: types.CallbackQuery):
    code = qiwi.codes['CNY']
    db.set_to(Data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()