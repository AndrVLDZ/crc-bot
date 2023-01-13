from db import get_currency_pair, get_round_state
from typing import List, Union
from dataclasses import dataclass, field
from requests import Session


@dataclass
class Data:
    rates: List[dict] = field(default_factory=list)


# dict of all currency codes supported by QIWI
CODES: dict = {
    "RUB": "643", 
    "USD": "840", 
    "EUR": "978", 
    "KZT": "398", 
    "CNY": "156",
}


# getting all exchange rates via QIWI API
async def get_rates(token: str):
    s = Session()
    s.headers = {"content-type": "application/json"}
    s.headers["authorization"] = "Bearer " + token
    s.headers["User-Agent"] = "Android v3.2.0 MKT"
    s.headers["Accept"] = "application/json"
    res = s.get("https://edge.qiwi.com/sinap/crossRates")
    Data.rates = res.json()["result"]


async def get_rate(user_id: int, converter: bool = False) -> Union[bool, float]:
    # getting currency codes
    curr_from, curr_to = await get_currency_pair(user_id)
    curr_from, curr_to = CODES[curr_from], CODES[curr_to]
    
    # requested exchange rate
    rate = [
        x for x in Data.rates
            if x["from"] == curr_from and 
            x["to"] == curr_to
    ]
    
    if len(rate) == 0:
        return False
    if converter: 
        return float(rate[0]["rate"])
    
    # getting user settings
    round_state = await get_round_state(user_id)
    if round_state:
        return round(rate[0]["rate"], 4)
    
    return rate[0]["rate"]

