import menu
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import db
import qiwi

router = Router() 

# /start command handler
@router.message(Command(commands=["start"]))
async def cmd_start(message: Message) -> None:
        user_id = message.from_user.id
        qiwi.Data.user_id = user_id
        user_name = message.from_user.first_name
        user_surname = message.from_user.last_name
        username = message.from_user.username
        if db.check_user(user_id):
                # start message for old user
                await message.answer(f'''
                Welcome back, {user_name}!\nYour last currencies settings applied''', 
                reply_markup=menu.main_menu)
        else: 
                db.add_user(user_id, user_name, user_surname, username)
                # start message for new user
                await message.answer(f"Welcome, {user_name}!")
                await message.answer('''
                This is a bot for monitoring exchange rates and converting at the QIWI internal rate''', 
                reply_markup=menu.main_menu)

