import menu
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import db

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_surname = message.from_user.last_name
    username = message.from_user.username
    
    if db.check_user(user_id):
        curr_from, curr_to = db.get_currency_pair(user_id)
        # start message for old user
        await message.answer(
            f"Welcome back, {user_name}! \
                \nYour last currencies settings: \
                    \nBuy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
            parse_mode="Markdown",
            reply_markup=menu.main_menu(),
        )
    else:
        db.add_user(user_id, user_name, user_surname, username)
        # start message for new user
        await message.answer(
            f"Welcome, {user_name}! \
                \nI can show the exchange rates of the QIWI Wallet \
                    \nAnd I also have a currency converter",
            reply_markup=menu.main_menu(),
        )
