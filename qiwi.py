from typing import List
from dataclasses import dataclass, field
import requests
import db


@dataclass
class Data:
    rates: List[dict] = field(
        default_factory=list, compare=False, hash=False, repr=False
    )
    rate: float = field(default=0)


# dict for storing currency codes
CODES: dict = {
    "RUB": "643", 
    "USD": "840", 
    "EUR": "978", 
    "KZT": "398", 
    "CNY": "156"
    }


# getting key by value from dictionary
def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


# function to get all exchange rates through QIWI API
async def get_rates(token):
    s = requests.Session()
    s.headers = {"content-type": "application/json"}
    s.headers["authorization"] = "Bearer " + token
    s.headers["User-Agent"] = "Android v3.2.0 MKT"
    s.headers["Accept"] = "application/json"
    res = s.get("https://edge.qiwi.com/sinap/crossRates")
    Data.rates = res.json()["result"]


# currency pair exchange rate
async def get_rate(user_id: int) -> str:
    # requested exchange rate
    rate = [
        x
        for x in Data.rates
        if x["from"] == db.get_from(user_id) and x["to"] == db.get_to(user_id)
    ]
    if len(rate) == 0:
        return False
    else:
        Data.rate = rate[0]["rate"]
        return True


async def converter(user_id: int, value: float, round_res: bool = True) -> str:
    await get_rate(user_id)
    if round_res:
        res = round(value * Data.rate, 2)
    else:
        res = value * Data.rate
    return res
