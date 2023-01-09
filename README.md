# QIWI CRC Bot

![info picture](/CRC_Description_git.png)  

## About  

Telegram bot with a currency converter with a built-in calculator and monitoring of exchange rates for the QIWI Wallet.  
Exchange rates are updated every minute via QIWI API.

See running bot: [@QIWI_CRC_bot](https://t.me/QIWI_CRC_bot "QIWI Converter Rate Calculator")

## Features

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
* requests 2.28.1
* sqlite3
* cexprtk 0.4.0

P.S. The list of libraries that must be installed to run the bot is in requirements.txt

## How to run

To start the bot, you need to specify two tokens:

* Telegram Bot API Token — [Get token](https://t.me/BotFather "Telegram BotFather")
* QIWI API Token — [Get token](https://qiwi.com/api "QIWI API")

The get_tokens.py script allows you to get tokens from .txt files or environment variables. This script is written to get tokens from .txt files when the bot is running locally or from environment variables when you want to deploy the bot.

### Run locally  

1. Create qiwi_token.txt and add to file your QIWI API token  
2. Create tg_token.txt and add to file your telegram bot API token
3. Run bot.py

P.S. All tokens and database are hidden in gitignore

``` gitignore
# ignore secret config
bot_token.txt
qiwi_token.txt
bot.sqlite
```

### Deploy via  [Railway](https://railway.app/ "Deploy to the cloud")

List all libraries in requirements.txt  

``` requirements.txt
aiogram==3.0.0b6
asyncio_periodic==2019.2
periodic==2.1.1
requests==2.28.1
cexprtk==0.4.0
```

Specify the entry point(bot.py) in the proc file

``` Procfile
web: python bot.py
```  

## Modules  

* bot — the main script that runs a bot polling, a scheduler for updating exchange rates and includes message handlers from all other modules through the router  
* get_tokens.py — getting Telegram Bot API and QIWI API tokens from environment variables (for deploy) or .txt files (for local run)  
* db — creating a database and working with it  
* qiwi — work with QIWI API, getting rate from QIWI API answer, conversion and calculation functionality  
* menu — menu markup generation  
* tools — user validation  
* h_start — start command handler  
* h_help — help command handler  
* h_about — about command handler and inline link-buttons  
* h_round — **Round** menu button handler  
* h_set_currencies — **Set currencies** menu button handler and inline buttons generation
* h_rate — **Rate** menu button handler  
* h_converter — **converter** handler
