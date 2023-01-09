# QIWI CRC Bot

![info picture](/CRC_Description_git.png)  

## About  

Telegram bot with a currency converter with a built-in calculator and monitoring of exchange rates for the QIWI Wallet.  
Exchange rates are updated every minute.

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

## How to run?

To start the bot, you need to specify two tokens:

* Telegram Bot API Token — [Get token](https://t.me/BotFather "Telegram BotFather")
* QIWI API Token — [Get token](https://qiwi.com/api "QIWI API")

The get_tokens.py script allows you to get tokens from .txt files or environment variables. This script is written to get tokens from .txt files when the bot is running locally or from environment variables when you want to deploy the bot.

### Local run  

1. Create qiwi_token.txt and add to file your QIWI API token  
2. Create tg_token.txt and add to file your telegram bot API token
3. Run bot.py

P.S. All tokens and database are hidden in gitignore.

``` gitignore
# ignore secret config
bot_token.txt
qiwi_token.txt
bot.sqlite
```

### Deploy via  [Railway](https://railway.app/ "Deploy to the cloud")

1. List all libraries in requirements.txt  
2. Specify the entry point(bot.py) in the proc file

``` requirements.txt
aiogram==3.0.0b6
asyncio_periodic==2019.2
periodic==2.1.1
requests==2.28.1
cexprtk==0.4.0
```

``` Procfile
web: python bot.py
```  

## Modules  

1. bot.py — the main script that runs a bot polling, a scheduler for updating exchange rates and includes message handlers from all other modules through the router  
2. get_tokens.py — getting Telegram Bot API and QIWI API tokens from environment variables (for deploy) or .txt files (for local run)  
3. db.py — creating a database and working with it  
4. qiwi.py — work with QIWI API, getting rate from QIWI API answer, conversion and calculation functionality  
5. menu.py — menu markup generation  
6. tools.py — user validation  
7. h_start.py — start command handler  
8. h_help.py — help command handler  
9. h_about.py — about command handler and inline link-buttons  
10. h_round.py — **Round** menu button handler  
11. h_set_currencies.py` — **Set currencies** menu button handler and inline buttons generation
12. h_rate.py — **Rate** menu button handler  
13. h_converter.py — **converter** handler
