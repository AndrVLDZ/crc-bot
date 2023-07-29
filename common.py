from typing import Union

from aiogram.types import Message, User

from db import user_in_db
from logs import log

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
'XDR': '🌐','XOF': '🇨🇮','XPF': '🇵🇫','YER': '🇾🇪',
'ZMW': '🇿🇲','ZWL': '🇿🇼','IMP': '🇮🇲','MXN': '🇲🇽',
'TVD': '🇹🇻', 'SLE': '🇸🇱',
}


async def get_first_name(message: Message) -> Union[str, bool]:
    if isinstance(message.from_user, User):
        return message.from_user.first_name
    log.info("First name not defined")
    return False


async def get_id(message: Message) -> int:
    if isinstance(message.from_user, User):
        return message.from_user.id 
    log.info("User not defined")
    return False


async def check_user(message: Message) -> Union[bool, int]: 
    telegram_user_id = await get_id(message)
    if telegram_user_id is not False:
        # if the user is not in the database
        if not await user_in_db(telegram_user_id):
            await message.answer(
                "Send `/start` command first!",
                parse_mode="Markdown"
            )
            return False
        # if the user is in the database 
        return telegram_user_id
    return False
