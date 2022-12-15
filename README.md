# QIWI Exchange Bot

![info picture](/description.png)

## About  

Telegram bot with a currency converter and monitoring of exchange rates for the QIWI Wallet.  
Exchange rates are updated every minute through a request to the QIWI API.

## What can?

* Currency selection
* Saving the selected currencies to apply the next time the user write
* Send the exchange rate of selected currencies
* Convert given amount with selected currencies  

## Technology stack  & libraries

* Python 3.10.8
* Aiogram 3.0.0b6
* QWI API
* asyncio
* sqlite3  
* requests

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
7. h_set_currencies.py  
8. h_rate.py  
9. h_converter.py
10. h_about.py  
