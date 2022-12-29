from typing import List
from dataclasses import dataclass, field
import requests
import db
from cexprtk import evaluate_expression


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
    s = requests.Session()
    s.headers = {"content-type": "application/json"}
    s.headers["authorization"] = "Bearer " + token
    s.headers["User-Agent"] = "Android v3.2.0 MKT"
    s.headers["Accept"] = "application/json"
    res = s.get("https://edge.qiwi.com/sinap/crossRates")
    Data.rates = res.json()["result"]


async def get_rate(user_id: int, converter: bool = False) -> str:
    # getting currency codes
    curr_from, curr_to = await db.get_currency_pair(user_id)
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
        return rate[0]["rate"]
    
    # getting user settings
    round_state = await db.get_round_state(user_id)
    if round_state:
        return round(rate[0]["rate"], 4)
    
    return rate[0]["rate"]


async def converter(user_id: int, value: float, round_res: bool) -> str:
    rate = await get_rate(user_id, converter=True)
    if not rate:
        return False 
    if round_res:
        res = evaluate_expression(value, {})
        return round(res*rate, 4)
    return evaluate_expression(value, {})*rate
