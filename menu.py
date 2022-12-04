from aiogram import types
from dataclasses import dataclass


@dataclass(frozen=True)
class data:
    main_menu = [
        [
            types.KeyboardButton(text="Rate"),
            types.KeyboardButton(text="Converter"),
            types.KeyboardButton(text="Set currencies"),
            types.KeyboardButton(text="About"),
        ],
    ]

    converter_round_off = [
        [
            types.KeyboardButton(text="Round: off"),
            types.KeyboardButton(text="Set currencies"),
            types.KeyboardButton(text="Back"),
        ],
    ]

    converter_round_on = [
        [
            types.KeyboardButton(text="Round: on"),
            types.KeyboardButton(text="Set currencies"),
            types.KeyboardButton(text="Back"),
        ],
    ]


main_menu = types.ReplyKeyboardMarkup(
    keyboard=data.main_menu,
    resize_keyboard=True,
    width=2,
    input_field_placeholder="Use buttons",
)

converter_round_off = types.ReplyKeyboardMarkup(
    keyboard=data.converter_round_off,
    resize_keyboard=True,
    width=2,
    input_field_placeholder="Enter value",
)

converter_round_on = types.ReplyKeyboardMarkup(
    keyboard=data.converter_round_on,
    resize_keyboard=True,
    width=2,
    input_field_placeholder="Enter value",
)
