from tools import check_user, get_id
from menu import main_menu
from db import get_currency_pair, set_currency_pair, set_from, set_to, get_from, get_to
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters import Command
from typing import Callable, Union
from bot import bot

router = Router()

# all currencies supported by exchangerate-api with flags
CURRENCIES = {
'USD': '🇺🇸','EUR': '🇪🇺','JPY': '🇯🇵','GBP': '🇬🇧',
'AUD': '🇦🇺','CAD': '🇨🇦','RUB': '🇷🇺','KZT': '🇰🇿',
'CHF': '🇨🇭','CNY': '🇨🇳','SEK': '🇸🇪','NZD': '🇳🇿',
'AED': '🇦🇪','SGD': '🇸🇬','HKD': '🇭🇰','NOK': '🇳🇴',
'KRW': '🇰🇷','TRY': '🇹🇷','INR': '🇮🇳','ZAR': '🇿🇦',
'BRL': '🇧🇷','DKK': '🇩🇰','PLN': '🇵🇱','TWD': '🇹🇼',
'THB': '🇹🇭','HUF': '🇭🇺','CZK': '🇨🇿','RON': '🇷🇴',
'ISK': '🇮🇸','BGN': '🇧🇬','HRK': '🇭🇷','ILS': '🇮🇱',
'MYR': '🇲🇾','PHP': '🇵🇭','IDR': '🇮🇩','AFN': '🇦🇫',
'ALL': '🇦🇱','AMD': '🇦🇲','ANG': '🇦🇼','AOA': '🇦🇴',
'ARS': '🇦🇷','AWG': '🇦🇼','AZN': '🇦🇿','BAM': '🇧🇦',
'BBD': '🇧🇧','BDT': '🇧🇩','BHD': '🇧🇭','BIF': '🇧🇮',
'BMD': '🇧🇲','BND': '🇧🇳','BOB': '🇧🇴','BSD': '🇧🇸',
'BTN': '🇧🇹','BWP': '🇧🇼','BYN': '🇧🇾','BZD': '🇧🇿',
'CDF': '🇨🇩','CLP': '🇨🇱','COP': '🇨🇴','CRC': '🇨🇷',
'CUP': '🇨🇺','CVE': '🇨🇻','DJF': '🇩🇯','DOP': '🇩🇴',
'DZD': '🇩🇿','EGP': '🇪🇬','ERN': '🇪🇷','ETB': '🇪🇹',
'FJD': '🇫🇯','FKP': '🇫🇰','FOK': '🇫🇴', 'GEL': '🇬🇪',
'GGP': '🇬🇬','GHS': '🇬🇭','GIP': '🇬🇮','GMD': '🇬🇲',
'GNF': '🇬🇳','GTQ': '🇬🇹','GYD': '🇬🇾','HNL': '🇭🇳',
'HTG': '🇭🇹','IQD': '🇮🇶','IRR': '🇮🇷','JEP': '🇯🇪',
'JMD': '🇯🇲','JOD': '🇯🇴','KES': '🇰🇪','KGS': '🇰🇬',
'KHR': '🇰🇭','KID': '🇰🇮','KMF': '🇰🇲','KWD': '🇰🇼',
'KYD': '🇰🇾','LAK': '🇱🇦','LBP': '🇱🇧','LKR': '🇱🇰',
'LRD': '🇱🇷','LSL': '🇱🇸','LYD': '🇱🇾','MAD': '🇲🇦',
'MDL': '🇲🇩','MGA': '🇲🇬','MKD': '🇲🇰','MMK': '🇲🇲',
'MNT': '🇲🇳','MOP': '🇲🇴','MRU': '🇲🇷','MUR': '🇲🇺',
'MVR': '🇲🇻','MWK': '🇲🇼','MZN': '🇲🇿','NAD': '🇳🇦',
'NGN': '🇳🇬','NIO': '🇳🇮','NPR': '🇳🇵','OMR': '🇴🇲',
'PAB': '🇵🇦','PEN': '🇵🇪','PGK': '🇵🇬','PKR': '🇵🇰',
'PYG': '🇵🇾','QAR': '🇶🇦','RSD': '🇷🇸','RWF': '🇷🇼',
'SAR': '🇸🇦','SBD': '🇸🇧','SCR': '🇸🇨','SDG': '🇸🇩',
'SHP': '🇸🇭','SLL': '🇸🇱','SOS': '🇸🇴','SRD': '🇸🇷',
'SSP': '🇸🇸','STN': '🇸🇹','SYP': '🇸🇾','SZL': '🇸🇿',
'TJS': '🇹🇯','TMT': '🇹🇲','TND': '🇹🇳','TOP': '🇹🇴',
'TTD': '🇹🇹','TZS': '🇹🇿','UAH': '🇺🇦','UGX': '🇺🇬',
'UYU': '🇺🇾','UZS': '🇺🇿','VES': '🇻🇪','VND': '🇻🇳',
'VUV': '🇻🇺','WST': '🇼🇸','XAF': '🇨🇲','XCD': '🇦🇬',
'XDR': 'un','XOF': '🇨🇮','XPF': '🇵🇫','YER': '🇾🇪',
'ZMW': '🇿🇲','ZWL': '🇿🇼','IMP': '🇮🇲','MXN': '🇲🇽',
'TVD': '🇹🇻', 'SLE': '🇸🇱',
}

class CurrencyCB(CallbackData, prefix="currency_callback"):
    chat_id: int # telegram chat ID
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From" 
    currency: str  # e.g. "USD", "RUB", ...


class PageCB(CallbackData, prefix="page_callback"):
    chat_id: int # telegram chat ID
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From" 
    page: int  # page number


def generate_curr_buttons(chat_id: int, user_id: int, pref: str, page: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    # calculate start and end index for slicing CURRENCIES
    start = page * 12
    end = start + 12

    # creating rows with 4 buttons
    for i in range(start, end, 4):
        buttons = []
        for curr, flag in list(CURRENCIES.items())[i:i+4]:
            cb_data = CurrencyCB(
                chat_id=chat_id,
                user_id=user_id,
                conv_prefix=pref,
                currency=f"{curr} {flag}",
            )
            buttons.append(
                InlineKeyboardButton(
                    text=f"{curr} {flag}", 
                    callback_data=cb_data.pack()
                )
            )
        builder.row(*buttons)
    
    # add navigation buttons if necessary
    nav_buttons = []
    if page > 0:
        # add 'Back' button
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
        # add 'Next' button
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


async def generate_swap_button(chat_id: int, user_id: int) -> KeyboardBuilder:
    swap_button = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="↔️",
            callback_data=CurrencyCB(
                chat_id=chat_id,
                user_id=user_id,
                conv_prefix="Swap",
                currency="",
            ).pack(),
        )
    )
    return swap_button


async def validate_user_curr(user_id: str, curr: str, get_func: Callable, set_func: Callable, pair: bool) -> Union[str, bool]:
    db_curr = await get_func(user_id)

    if curr == db_curr.split()[0]:
        if pair:
            return False
        return f"Currency **{curr}** has already been set"

    if curr in CURRENCIES.keys():
        flag = CURRENCIES[curr]
        await set_func(user_id, f"{curr} {flag}")
        if pair:
            return True
        return f"Currency **{curr} {CURRENCIES[curr]}** successfully set"
    
    return f"No such currency **{curr}**"


@router.message(Command(commands=["from"]))
async def cmd_set_from(message: Message, command: Command) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        if command.args:
            curr_from = str((command.args.split())[0]).upper()
            response_text = await validate_user_curr(user_id, curr_from, get_from, set_from, pair=False)
            menu = await main_menu(user_id)
            await message.answer(
                text=response_text,
                parse_mode="Markdown",
                reply_markup=menu,
            )
        else:
            menu = await main_menu(user_id)
            await message.answer("Specify currency", reply_markup=menu)


@router.message(Command(commands=["to"]))
async def cmd_set_to(message: Message, command: Command) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        if command.args:
            curr_to = str((command.args.split())[0]).upper()
            response_text = await validate_user_curr(user_id, curr_to, get_to, set_to, pair=False)
            menu = await main_menu(user_id)
            await message.answer(
                text=response_text,
                parse_mode="Markdown",
                reply_markup=menu,
            )
        else:
            menu = await main_menu(user_id)
            await message.answer("Specify currency", reply_markup=menu)


@router.message(Command(commands=["pair"]))
async def cmd_set_pair(message: Message, command: Command) -> None:
    user_id = await get_id(message)
    menu = await main_menu(user_id)
    if await check_user(message):
        if command.args and len((command.args.split())) == 2:
            args = command.args.split()
            curr_from = str(args[0]).upper()
            curr_to = str(args[1]).upper()

            to_response_text = await validate_user_curr(user_id, curr_to, get_to, set_to, pair=True)
            from_response_text = await validate_user_curr(user_id, curr_from, get_from, set_from, pair=True)

            if not to_response_text and not from_response_text:
                await message.answer(
                    text=f"**{curr_from} {CURRENCIES[curr_from]}** >> **{curr_to} {CURRENCIES[curr_to]}**", 
                    parse_mode="Markdown",
                    reply_markup=menu
                )

            if to_response_text and not from_response_text:
                await message.answer(
                    text=f"**{curr_from}** >> **{curr_to}**", 
                    parse_mode="Markdown",
                    reply_markup=menu
                )
        else:
            await message.answer("Specify currency pair", reply_markup=menu)


@router.message(Command(commands=["swap"]))
async def cmd_swap(message: Message) -> None:
    if await check_user(message):
        user_id = await get_id(message)
        curr_from, curr_to = await get_currency_pair(user_id)
        await set_currency_pair(user_id, curr_to, curr_from)
        menu = await main_menu(user_id)
        await message.answer(
            text=f"**{curr_to}** >> **{curr_from}**", 
            parse_mode="Markdown",
            reply_markup=menu
        )
    

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
            reply_markup=menu
        )
        await bot.delete_message(chat_id, message.message_id)



@router.message(F.text.startswith("Set currencies"))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:

        curr_from = generate_curr_buttons(chat_id, user_id, "From", 0)
        await message.answer("From", reply_markup=curr_from.as_markup())

        curr_to = generate_curr_buttons(chat_id, user_id, "To", 0)
        await message.answer("To", reply_markup=curr_to.as_markup())


@router.message(F.text.startswith("From: "))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:

        curr_from = generate_curr_buttons(chat_id, user_id, "From", 0)
        await message.answer("From", reply_markup=curr_from.as_markup())
        
        await bot.delete_message(chat_id, message.message_id)



@router.message(F.text.startswith("To: "))
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    chat_id = message.chat.id
    if user_id:

        curr_to = generate_curr_buttons(chat_id, user_id, "To", 0)
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
    if prefix == 'Swap':
        curr_from, curr_to = await get_currency_pair(user_id)
        await set_currency_pair(user_id, curr_to, curr_from)

    curr_from, curr_to = await get_currency_pair(user_id)
    menu = await main_menu(user_id)
    await bot.send_message(
        chat_id=chat_id,
        text=f"{curr_from} >> {curr_to}", 
        parse_mode="Markdown",
        reply_markup=menu
    )

    await callback.answer()


@router.callback_query(PageCB.filter())
async def pagination_handler(query: CallbackQuery, callback_data: PageCB):
    # getting data from callback_data
    prefix = callback_data.conv_prefix
    page = callback_data.page
    chat_id = callback_data.chat_id
    user_id = callback_data.user_id

    # Generate the new buttons
    curr_buttons = generate_curr_buttons(chat_id, user_id, prefix, page)

    # Edit the message to show the new buttons
    await query.message.edit_reply_markup(reply_markup=curr_buttons.as_markup())

    # Always answer callback queries, even if you don't update the message
    await query.answer()
