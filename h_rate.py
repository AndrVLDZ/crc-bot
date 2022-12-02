import db
import qiwi
from aiogram import types, F, Router

router = Router() 

@router.message(F.text == "Rate")
async def rate(message: types.Message):
    user_id = message.from_user.id
    qiwi.Data.user_id = user_id
    if db.check_user(user_id):
        if  await qiwi.get_rate(user_id): 
            currency_from = qiwi.get_key(qiwi.codes, db.get_from(user_id))
            currency_to = qiwi.get_key(qiwi.codes, db.get_to(user_id))
            if currency_from != currency_to: 
                await message.answer(f"For 1 {currency_to} you will pay *{qiwi.Data.rate}* {currency_from} ",  parse_mode= 'Markdown')
            elif currency_from == currency_to: 
                await message.answer("Currency *from* is equal to currency *to*, set different values!",  parse_mode= 'Markdown')
        else:
            await message.answer("Set currencies!")
    else:
        await message.answer("Send `/start` command and set currencies!", parse_mode= 'Markdown')
