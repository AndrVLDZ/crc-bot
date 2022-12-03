import db
import qiwi
from aiogram import types, F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


router = Router()

# All currencies supported by QIWI
CURRENCIES = ["USD", "EUR", "RUB", "KZT", "CNY"]


class CurrencyCB(CallbackData, prefix="curr_pair"):
    user_id: int
    curr_str: str # e.g. "to_RUB" or "from_USD" 


@router.message(F.text == "Set currencies")
async def set_currency_pair(message: types.Message):
    def add_buttons(builder: InlineKeyboardBuilder, data_prefix):
        for curr in CURRENCIES:
            data = CurrencyCB(
                user_id=message.from_user.id,
                curr_str=f"{data_prefix}_{curr}"
            )
            
            builder.add(
                types.InlineKeyboardButton(
                    text=curr,
                    callback_data=data.pack()
                )
            )

    curr_from = InlineKeyboardBuilder()
    add_buttons(curr_from, data_prefix="from")
    await message.answer("I have", reply_markup=curr_from.as_markup())

    curr_to = InlineKeyboardBuilder()
    add_buttons(curr_to, data_prefix="to")
    await message.answer("I want to buy", reply_markup=curr_to.as_markup())

@router.callback_query(CurrencyCB.filter(F.curr_str == 'from_USD'))
async def from_usd(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['USD']
    db.set_from(callback_data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()  

@router.callback_query(CurrencyCB.filter(F.curr_str == 'to_USD'))
async def to_usd(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['USD']
    db.set_to(callback_data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'from_EUR'))
async def from_eur(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['EUR']
    db.set_from(callback_data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'to_EUR'))
async def to_eur(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['EUR']
    db.set_to(callback_data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'from_RUB'))
async def from_rub(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['RUB']
    db.set_from(callback_data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'to_RUB'))
async def to_rub(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['RUB']
    db.set_to(callback_data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'from_KZT'))
async def from_kzt(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['KZT']
    db.set_from(callback_data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'to_KZT'))
async def to_kzt(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['KZT']
    db.set_to(callback_data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'from_CNY'))
async def from_cny(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['CNY']
    db.set_from(callback_data.user_id, code)
    await callback.message.answer(f'Currency from has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()

@router.callback_query(CurrencyCB.filter(F.curr_str == 'to_CNY'))
async def to_cny(callback: types.CallbackQuery, callback_data: CurrencyCB):
    code = qiwi.codes['CNY']
    db.set_to(callback_data.user_id, code)
    await callback.message.answer(f'Currency to has been set to {qiwi.get_key(qiwi.codes, code)}')
    await callback.answer()
