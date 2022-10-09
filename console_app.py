from dataclasses import dataclass
import requests
import qiwi_tkn

@dataclass(frozen=True)
class data:
    # currency codes
    RUB: str = '643'
    USD: str = '840'
    EUR: str = '978'
    KZT: str = '398'
    ОКВ: str = '156'


def print_logo(logo=''):
    LOGO_DAFAULT = """
   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
   `      \(/|\)/        `
           " ` "
   QIWI_Exchange_By_VLDZ 
"""
    if logo != '':
        print(logo)
    else:
        print(LOGO_DAFAULT)

print_logo()

# currency pair exchange rate
def exchange(currency_to: str, currency_from: str): 
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + qiwi_tkn.api_access_token
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

if __name__ == '__main__':
    work: int = 1
    while work != 0:
        # getting a token
        qiwi_tkn.get()

        # input data
        currency_from: str = data.USD
        currency_to: str = data.RUB
        amount: float = float(input(('\n Доллары: ')))

        # conversion at the current QIWI rate
        answ = converter(currency_from, currency_to, amount)

        # output
        print(f' Курс QIWI: {answ[0]}')
        print(f' -> Рубли: {answ[1]}')