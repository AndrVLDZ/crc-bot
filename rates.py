import aiohttp
from typing import Union
from dataclasses import dataclass, field
from db import get_currency_pair, get_round_state


@dataclass
class Data:
    rates: dict = field(default_factory=dict)


# getting all exchange rates via exchangerate-api
async def get_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.exchangerate-api.com/v4/latest/USD") as response:
            if response.status == 200:
                data = (await response.json())["rates"]
                Data.rates = data
                    

async def get_rate(user_id: int, converter: bool = False) -> Union[bool, float]:
    # getting currency codes
    curr_from, curr_to = await get_currency_pair(user_id)
    curr_from = curr_from.split()[0]
    curr_to = curr_to.split()[0]

    # requested exchange rate
    if curr_from not in Data.rates or curr_to not in Data.rates:
        return False

    rate =  Data.rates[curr_to] / Data.rates[curr_from]
    if rate == 1.0:
        return False
    
    if converter: 
        return float(rate)
    
    # getting user settings
    round_state = await get_round_state(user_id)
    if round_state:
        return round(rate, 4)
    
    return rate