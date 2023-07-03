from tools import check_user, get_id
from menu import main_menu
from db import get_currency_pair, set_currency_pair, set_from, set_to, get_from, get_to, save_user_data, load_user_data
from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.methods.edit_message_text import EditMessageText
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.filters import Command

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
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From" 
    currency: str  # e.g. "USD", "RUB", ...


class PageCB(CallbackData, prefix="page_callback"):
    user_id: int  # telegram user ID
    conv_prefix: str  # e.g. "To" or "From" 
    page: int  # page number

def generate_curr_buttons(user_id: int, pref: str, page: int) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()

    # calculate start and end index for slicing CURRENCIES
    start = page * 10
    end = start + 10

    # creating rows with 4 buttons
    for i in range(start, end, 4):
        buttons = []
        for curr, flag in list(CURRENCIES.items())[i:i+4]:
            cb_data = CurrencyCB(
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



async def generate_swap_button(user_id) -> KeyboardBuilder:
    swap_button = InlineKeyboardBuilder().add(
        InlineKeyboardButton(
            text="↔️",
            callback_data=CurrencyCB(
                user_id=user_id,
                conv_prefix="Swap",
                currency="",
            ).pack(),
        )
    )
    return swap_button


async def generate_info_msg(user_id: int, message: Message):
    swap_button = await generate_swap_button(user_id)
    curr_from, curr_to = await get_currency_pair(user_id)
    info_msg = await message.answer(
        text=f"Buy:  **[{curr_to}]**    |    For:  **[{curr_from}]**",
        parse_mode="Markdown",
        reply_markup=swap_button.as_markup()
    )
    
    user_data = {
        "chat_id": info_msg.chat.id,
        "message_id": info_msg.message_id,
    }
    await save_user_data(user_id, user_data)


async def edit_info_msg(user_id: int):
    swap_button = await generate_swap_button(user_id)
    user_data = await load_user_data(user_id)
    curr_from, curr_to = await get_currency_pair(user_id)
    edit_message = EditMessageText(
        chat_id=user_data["chat_id"],
        message_id=user_data["message_id"],
        text=f"For:  **[{curr_from}]**    |    By:  **[{curr_to}]**",
        parse_mode="Markdown",
        reply_markup=swap_button.as_markup(),
    )
    return edit_message


@router.message(Command(commands=["for"]))
async def cmd_set_from(message: Message, command: Command) -> None:
    if await check_user(message):
        menu = await main_menu(user_id)
        if command.args:
            user_id = await get_id(message)
            curr_from = str((command.args.split())[0]).upper()
            db_from = await get_from(user_id)

            if curr_from == db_from.split()[0]:
                await message.answer(
                    text=f"Currency **{curr_from}** has already been set",
                    parse_mode="Markdown",
                    reply_markup=menu,
                )
                return
            
            if curr_from in CURRENCIES.keys():
                flag = CURRENCIES[curr_from]
                await set_from(user_id, f"{curr_from} {flag}")
            else:
                await message.answer("No such currency")
        else:
            await message.answer("Specify currency")
        await message.answer(
            text=f"Currency **{curr_from}** successfully set", 
            parse_mode="Markdown",
            reply_markup=menu,
        )
        return await edit_info_msg(user_id)


@router.message(Command(commands=["by"]))
async def cmd_set_to(message: Message, command: Command) -> None:
    if await check_user(message):
        menu = await main_menu(user_id)
        if command.args:
            user_id = await get_id(message)
            curr_to = str((command.args.split())[0]).upper()
            db_to = await get_to(user_id)

            if curr_to == db_to.split()[0]:
                await message.answer(
                    text=f"Currency **{curr_to}** has already been set",
                    parse_mode="Markdown",
                    reply_markup=menu,
                    )
                return
            
            if curr_to in CURRENCIES.keys():
                flag = CURRENCIES[curr_to]
                await set_to(user_id, f"{curr_to} {flag}")
            else:
                await message.answer("No such currency")
        else:
            await message.answer("Specify currency")
        await message.answer(
            text=f"Currency **{curr_to}** successfully set", 
            parse_mode="Markdown",
            reply_markup=menu,
        )
        return await edit_info_msg(user_id)


@router.message(Command(commands=["pair"]))
async def cmd_set_pair(message: Message, command: Command) -> None:
    user_id = await get_id(message)
    if await check_user(message):
        if command.args and len((command.args.split())) == 2:
            args = command.args.split()
            curr_from = str(args[0]).upper()
            curr_to = str(args[1]).upper()
            db_from, db_to = await get_currency_pair(user_id)

            if curr_from == db_from.split()[0]:
                await message.answer(
                    text=f"Currency **{curr_from}** has already been set",
                    parse_mode="Markdown",
                    reply_markup=menu,
                    )
                if curr_to == db_to.split()[0]:
                    await message.answer(
                        text=f"Currency **{curr_to}** has already been set",
                        parse_mode="Markdown",
                        reply_markup=menu,
                        )
                return
            
            if curr_from in CURRENCIES.keys():
                flag = CURRENCIES[curr_from]
                await set_from(user_id, f"{curr_from} {flag}")
            else:
                await message.answer("No such currency")
            if curr_to == db_to.split()[0]:
                await message.answer(
                    text=f"Currency **{curr_to}** has already been set",
                    parse_mode="Markdown",
                    reply_markup=menu,
                    )
                return
            
            if curr_to in CURRENCIES.keys():
                flag = CURRENCIES[curr_to]
                await set_to(user_id, f"{curr_to} {flag}")
            else:
                await message.answer("No such currency")
        else:
            await message.answer("Specify currency pair")
        menu = await main_menu(user_id)
        await message.answer(f"Currency pair {curr_from} >> {curr_to} successfully set", reply_markup=menu)
        return await edit_info_msg(user_id)



@router.message(F.text == "Set currencies")
async def currency_pair_chooser(message: Message):
    user_id = await check_user(message)
    if user_id:
        
        curr_from = generate_curr_buttons(user_id, "From", 0)
        await message.answer("My currency", reply_markup=curr_from.as_markup())

        curr_to = generate_curr_buttons(user_id, "To", 0)
        await message.answer("I want to buy", reply_markup=curr_to.as_markup())
        
        await generate_info_msg(user_id, message)


@router.callback_query(CurrencyCB.filter())
async def save_currency(callback: CallbackQuery, callback_data: CurrencyCB) -> EditMessageText:
    # getting data from callback_data
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
        
    await callback.answer()
    
    return await edit_info_msg(user_id)


@router.callback_query(PageCB.filter())
async def pagination_handler(query: CallbackQuery, callback_data: PageCB):
    # getting data from callback_data
    prefix = callback_data.conv_prefix
    page = callback_data.page
    user_id = callback_data.user_id

    # Generate the new buttons
    curr_buttons = generate_curr_buttons(user_id, prefix, page)

    # Edit the message to show the new buttons
    await query.message.edit_reply_markup(reply_markup=curr_buttons.as_markup())

    # Always answer callback queries, even if you don't update the message
    await query.answer()
