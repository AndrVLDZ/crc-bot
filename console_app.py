import logo
from dataclasses import dataclass
import get_tkn
import qiwi_tools

# default currency
currency_to = qiwi_tools.data.RUB

if __name__ == '__main__':
    logo.print_logo()
    work: int = 1
    while work != 0:
        # input data
        currency_to
        currency_from: str = qiwi_tools.data.USD
        amount: float = float(input(('\n Доллары: ')))
        # conversion at the current QIWI rate
        answ = qiwi_tools.converter(currency_from, currency_to, amount)
        # output
        print(f' Курс QIWI: {answ[0]}')
        print(f' -> Рубли: {answ[1]}')
