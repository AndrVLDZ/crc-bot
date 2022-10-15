from dataclasses import dataclass
import requests
import get_tkn

# getting a qiwi token
token = get_tkn.get('qiwi_token.txt')

@dataclass(frozen=True)
class data:
    # currency codes
    RUB: str = '643' 
    USD: str = '840' 
    EUR: str = '978' 
    KZT: str = '398'
    ОКВ: str = '156'

# currency pair exchange rate
def exchange(currency_to: str, currency_from: str): 
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    res = s.get('https://edge.qiwi.com/sinap/crossRates')

    # all exchange rates
    rates = res.json()['result']

    # requested exchange rate
    rate = [x for x in rates if x['from'] == currency_from and x['to'] == currency_to]
    if (len(rate) == 0):
        print('No rate for this currencies!')
        return
    else:
        return str(rate[0]['rate'])
        

def converter(currency_from: str,  currency_to: str, value: float, round_res: bool = True) -> list:
    exch: float = float(exchange(currency_from, currency_to))
    if round_res:
        res = [exch, round(value*exch, 2)]
    else:
        res = [exch, value*exch, 2]
    return res

