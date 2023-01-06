# QIWI CRC Bot

![info picture](/CRC_Description_git.png)  

## About  

Telegram bot with a converter, calculator and monitoring of QIWI Wallet exchange rates that are updated every minute.

See running bot: [@QIWI_CRC_bot](https://t.me/QIWI_CRC_bot "QIWI Converter Rate Calculator")

## What can?

* Set currency pair and rounding mode
* Solve math expressions before converting
* Convert a sent via message value or result of a sent math expression
* Send the exchange rate of selected currencies
* Save user settings (currency pair and rounding mode)

## Technology stack  & libraries

* Python 3.10.8
* Aiogram 3.0.0b6
* asyncio
* asyncio-periodic 2019.2
* QWI API
* requests 2.28.1
* sqlite3
* cexprtk 0.4.0

*P.S. The list of libraries that must be installed to run the bot is in requirements.txt.*

## Local run  

1. Create qiwi_token.txt and add to file your QIWI API token  
2. Create tg_token.txt and add to file your telegram bot API token
3. Run bot.py

The get_tkn.py module allows you to get tokens from .txt files, this script is written to run the bot locally and is not needed for deployment.  
  
*P.S. All tokens and database are hidden in gitignore.*

``` gitignore
# ignore secret config
qiwi_token.txt
tg_token.txt
```

## Deploy

The list of libraries that must be installed to run the bot is in requirements.txt.
To specify the entry point, you must specify the main script(bot.py) in the proc file

``` Procfile
web: python bot.py
```

For deployment in the bot.py module, you need to implement the receipt of tokens. I do not recommend using get_tkn.py and .txt files.  
This can be done in many different ways, but personally I use environment variables and the standard os library.  
Something like that:  

``` Python  
import os
qiwi_token = os.environ.get('QIWI_TOKEN')
tg_token = os.environ.get('BOT_TOKEN')
```

## Modules  

1. bot.py  
2. get_tkn.py  
3. db.py  
4. qiwi.py  
5. menu.py  
6. h_start.py  
7. h_round.py
8. h_set_currencies.py  
9. h_rate.py
10. h_converter.py
11. h_about.py
