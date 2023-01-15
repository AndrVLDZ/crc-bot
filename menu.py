from db import get_round_state
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def main_menu(user_id, new_user: bool = False):
    round_state = "on" if new_user or await get_round_state(user_id) else "off"
    
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="Rate"),
        KeyboardButton(text=f"Round: {round_state}"),
        width=2
    ) 
    
    builder.row(
        KeyboardButton(text="Set currencies"),
        width=1
    )
    
    main_menu_buttons = builder.export()
    
    main_menu = ReplyKeyboardMarkup(
        keyboard=main_menu_buttons,
        resize_keyboard=True,
        input_field_placeholder="Enter value",
    )
    
    return main_menu
