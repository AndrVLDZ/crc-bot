from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import db


async def main_menu(user_id, new_user: bool = False):
    round: str = ''
    if new_user:
        round = "on"
    else:
        round = "on" if await db.get_round_state(user_id) else "off"
    
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="Rate"),
        KeyboardButton(text=f"Round: {round}"),
        width=2
    ) 
    
    builder.row(
        KeyboardButton(text="Set currencies"),
        KeyboardButton(text="About"),
        width=1
    )
    
    main_menu_buttons = builder.export()
    
    main_menu = ReplyKeyboardMarkup(
        keyboard=main_menu_buttons,
        resize_keyboard=True,
        input_field_placeholder="Enter value to convert",
    )
    return main_menu

async def main_menu_new_user(user_id):
    builder = ReplyKeyboardBuilder()
    
    state = "on" if await db.get_round_state(user_id) else "off"
    builder.row(
        KeyboardButton(text="Rate"),
        KeyboardButton(text=f"Round: {state}"),
        width=2
    ) 
    
    builder.row(
        KeyboardButton(text="Set currencies"),
        KeyboardButton(text="About"),
        width=1
    )
    
    main_menu_buttons = builder.export()
    
    main_menu = ReplyKeyboardMarkup(
        keyboard=main_menu_buttons,
        resize_keyboard=True,
        input_field_placeholder="Enter value to convert",
    )
    return main_menu


# async def converter(user_id):
    
#     builder = ReplyKeyboardBuilder()
    
#     state = "on" if await db.get_round_state(user_id) else "off"
#     builder.row(
#         KeyboardButton(text=f"Round: {state}"),
#         KeyboardButton(text="Set currencies"),
#         width=2
#     )
    
#     builder.row(
#         KeyboardButton(text="Back"),
#         width=1
#     )
    
#     converter_buttons = builder.export()
        
#     converter = ReplyKeyboardMarkup(
#         keyboard=converter_buttons,
#         resize_keyboard=True,
#         input_field_placeholder="Enter value",
#     )
#     return converter
