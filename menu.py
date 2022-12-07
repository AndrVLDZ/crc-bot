from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import db


def main_menu():
    main_menu_buttons = ReplyKeyboardBuilder().row(
    KeyboardButton(text="Rate"),
    KeyboardButton(text="Converter"),
    KeyboardButton(text="Set currencies"),
    KeyboardButton(text="About"),
    width=2).export() 
    
    main_menu = ReplyKeyboardMarkup(
        keyboard=main_menu_buttons,
        resize_keyboard=True,
        input_field_placeholder="Use buttons",
    )
    return main_menu


def converter(user_id):
    state = "on" if db.get_round(user_id) else "off"
    converter_buttons = ReplyKeyboardBuilder().row(
        KeyboardButton(text=f"Round: {state}"),
        KeyboardButton(text="Set currencies"),
        KeyboardButton(text="Back"),
        width=2).export() 
        
    converter = ReplyKeyboardMarkup(
        keyboard=converter_buttons,
        resize_keyboard=True,
        input_field_placeholder="Enter value",
    )
    return converter
