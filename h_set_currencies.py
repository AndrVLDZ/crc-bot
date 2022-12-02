import db
import qiwi
from aiogram import types, F, Router
from aiogram.filters.text import Text
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dataclasses import dataclass, field

router = Router() 

@dataclass
class Data:
    user_id: int = field(default=0)


@router.message(F.text == 'Set currencies')
async def set_currency_from(message: types.Message):
    Data.user_id = message.from_user.id
    builder1 = InlineKeyboardBuilder()
    builder1.add(types.InlineKeyboardButton(
        text='USD',
        callback_data='from_USD',
        user_id = message.from_user.id)
    )
    builder1.add(types.InlineKeyboardButton(
        text="EUR",
        callback_data='from_EUR')
    )
    builder1.add(types.InlineKeyboardButton(
        text="RUB",
        callback_data='from_RUB')
    )
    builder1.add(types.InlineKeyboardButton(
        text="KZT",
        callback_data='from_KZT')
    )
    builder1.add(types.InlineKeyboardButton(
        text="CNY",
        callback_data='from_CNY')
    )
    await message.answer(
        "I have",
        reply_markup=builder1.as_markup()
    )

    builder2 = InlineKeyboardBuilder()
    builder2.add(types.InlineKeyboardButton(
        text="USD",
        callback_data="to_USD")
    )
    builder2.add(types.InlineKeyboardButton(
        text="EUR",
        callback_data="to_EUR")
    )
    builder2.add(types.InlineKeyboardButton(
        text="RUB",
        callback_data="to_RUB")
    )
    builder2.add(types.InlineKeyboardButton(
        text="KZT",
        callback_data="to_KZT")
    )
    builder2.add(types.InlineKeyboardButton(
        text="CNY",
        callback_data="to_CNY")
    )
    await message.answer(
        "I want to buy",
        reply_markup=builder2.as_markup()
    )

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