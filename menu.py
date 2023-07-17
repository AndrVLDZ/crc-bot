from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from db import get_currency_pair, get_round_state
from rates import get_rate


async def main_menu(user_id: int, new_user: bool = False) -> ReplyKeyboardMarkup:
    round_state = "on" if new_user or await get_round_state(user_id) else "off"
    curr_from, curr_to = (
        ("USD 🇺🇸", "EUR 🇪🇺") if new_user else await get_currency_pair(user_id)
    )
    rate = "Tap to find out" if new_user else await get_rate(user_id)

    builder = ReplyKeyboardBuilder()

    builder.row(
        KeyboardButton(text=f"Rate: {rate}"),
        KeyboardButton(text=f"Round: {round_state}"),
        width=2,
    )

    builder.row(
        KeyboardButton(text=f"From: {curr_from}"),
        KeyboardButton(text=f"To: {curr_to}"),
        width=3,
    )

    builder.row(KeyboardButton(text=f"↔️"), width=1)

    main_menu_buttons = builder.export()

    main_menu = ReplyKeyboardMarkup(
        keyboard=main_menu_buttons,
        resize_keyboard=True,
        input_field_placeholder="Value or math expr",
    )

    return main_menu
