from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.bot import bot
from common.checks import check_user, get_id
from common.currencies import CURRENCIES
from db import get_currency_pair, set_currency_pair, set_from, set_to
from menu import main_menu

router = Router()


class CurrencyCB(CallbackData, prefix="currency_callback"):
    chat_id: int  # telegram chat ID
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From"
    currency: str  # e.g. "USD", "RUB", ...


class PageCB(CallbackData, prefix="page_callback"):
    chat_id: int  # telegram chat ID
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From"
    page: int  # page number


async def generate_curr_buttons(
    chat_id: int, user_id: int, pref: str, page: int
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    # calculate start and end index for slicing CURRENCIES
    start = page * 12
    end = start + 12

    # creating rows with 4 buttons
    for i in range(start, end, 4):
        buttons = []
        for curr, flag in list(CURRENCIES.items())[i : i + 4]:
            cb_data = CurrencyCB(
                chat_id=chat_id,
                user_id=user_id,
                conv_prefix=pref,
                currency=f"{curr} {flag}",
            )
            buttons.append(
                InlineKeyboardButton(
                    text=f"{curr} {flag}", callback_data=cb_data.pack()
                )
            )
        builder.row(*buttons)

    nav_buttons = []
    if page > 0:
        # adding a 'Back' button
        back_data = PageCB(
            chat_id=chat_id,
            user_id=user_id,
            conv_prefix=pref,
            page=page - 1,
        )
        nav_buttons.append(
            InlineKeyboardButton(
                text="<< Back",
                callback_data=back_data.pack(),
            )
        )

    if len(CURRENCIES) > end:
        # add a 'Next' button
        next_data = PageCB(
            chat_id=chat_id,
            user_id=user_id,
            conv_prefix=pref,
            page=page + 1,
        )
        nav_buttons.append(
            InlineKeyboardButton(
                text="Next >>",
                callback_data=next_data.pack(),
            )
        )
    builder.row(*nav_buttons)

    return builder


@router.message(F.text == "↔️")
async def cmd_swap(message: Message) -> None:
    if await check_user(message):
        chat_id = message.chat.id
        user_id = await get_id(message)
        curr_from, curr_to = await get_currency_pair(user_id)
        await set_currency_pair(user_id, curr_to, curr_from)
        menu = await main_menu(user_id)
        await message.answer(
            text=f"**{curr_to}** >> **{curr_from}**",
            parse_mode="Markdown",
            reply_markup=menu,
        )
        await bot.delete_message(chat_id, message.message_id)


@router.message(F.text.startswith("Set currencies"))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:
        curr_from = await generate_curr_buttons(chat_id, user_id, "From", 0)
        await message.answer("From", reply_markup=curr_from.as_markup())

        curr_to = await generate_curr_buttons(chat_id, user_id, "To", 0)
        await message.answer("To", reply_markup=curr_to.as_markup())


@router.message(F.text.startswith("From: "))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:
        curr_from = await generate_curr_buttons(chat_id, user_id, "From", 0)
        await message.answer("From", reply_markup=curr_from.as_markup())

        await bot.delete_message(chat_id, message.message_id)


@router.message(F.text.startswith("To: "))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:
        curr_to = await generate_curr_buttons(chat_id, user_id, "To", 0)
        await message.answer("To", reply_markup=curr_to.as_markup())

        await bot.delete_message(chat_id, message.message_id)


@router.callback_query(CurrencyCB.filter())
async def save_currency(callback: CallbackQuery, callback_data: CurrencyCB):
    # getting data from callback_data
    chat_id = callback_data.chat_id
    user_id = callback_data.user_id
    prefix = callback_data.conv_prefix
    currency = callback_data.currency

    if prefix == "From":
        await set_from(user_id, currency)
    if prefix == "To":
        await set_to(user_id, currency)

    curr_from, curr_to = await get_currency_pair(user_id)
    menu = await main_menu(user_id)
    await bot.send_message(
        chat_id=chat_id,
        text=f"{curr_from} >> {curr_to}",
        parse_mode="Markdown",
        reply_markup=menu,
    )

    await callback.answer()


@router.callback_query(PageCB.filter())
async def pagination_handler(callback: CallbackQuery, callback_data: PageCB):
    # getting data from callback_data
    prefix = callback_data.conv_prefix
    page = callback_data.page
    chat_id = callback_data.chat_id
    user_id = callback_data.user_id

    # generation of new buttons
    curr_buttons = await generate_curr_buttons(chat_id, user_id, prefix, page)

    # editing the message to display the new buttons
    await callback.message.edit_reply_markup(reply_markup=curr_buttons.as_markup())

    await callback.answer()
