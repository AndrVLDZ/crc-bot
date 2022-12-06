from typing import List
from dataclasses import dataclass, field
import requests
import db


@dataclass
class Data:
    rates: List[dict] = field(default_factory=list)


# dict for storing currency codes
CODES: dict = {
    "RUB": "643", 
    "USD": "840", 
    "EUR": "978", 
    "KZT": "398", 
    "CNY": "156"
    }


# function to get all exchange rates through QIWI API
async def get_rates(token):
    s = requests.Session()
    s.headers = {"content-type": "application/json"}
    s.headers["authorization"] = "Bearer " + token
    s.headers["User-Agent"] = "Android v3.2.0 MKT"
    s.headers["Accept"] = "application/json"
    res = s.get("https://edge.qiwi.com/sinap/crossRates")
    Data.rates = res.json()["result"]


async def get_rate(user_id: int) -> str:
    # requested exchange rate
    rate = [
        x
        for x in Data.rates
        if x["from"] == CODES[db.get_from(user_id)] and x["to"] == CODES[db.get_to(user_id)]
    ]
    if len(rate) == 0:
        return False
    else:
        return rate[0]["rate"]


async def converter(user_id: int, value: float, round_res: bool = True) -> str:
    rate = await get_rate(user_id)
    if round_res:
        res = round(value * rate, 2)
    else:
        res = value * rate
    return res
