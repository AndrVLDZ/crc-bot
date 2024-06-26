# CRC Bot

[![info picture](/CRC_git.png)](https://t.me/CRC2_bot)

## About

CRC Bot is a currency converter with built-in calculator and monitoring of exchange rates, which are updated every day via exchange-api.
The converter is always active, just send a number or math expression. The result of the expression will be automatically calculated and converted to the final currency.

See running bot: [@CRC2_bot](https://t.me/CRC2_bot "Converter Rate Calculator")

The bot is originally designed to be used when traveling for quick price orientation in stores and quick small calculations.
But later I realized that the bot is suitable not only for this purpose and added commands for working with currency pairs, which speeds up the work from the desktop.

Perhaps later I will add a subscription to notifications about currency pair rate changes with the ability to set threshold values.

## Features

* Setting the currency pair and rounding mode
* Solving a user-sent mathematical expressions before converting
* Converting a value sent via message or the result of a user-sent math expression
* Sending the exchange rate of the currency pair
* Saving user settings in database (currency pair and rounding mode)

## Dependencies

* python-dotenv 1.0.1
* python 3.11.4
* aiogram 3.1.1
* aiosqlite 0.19.0
* aiohttp 3.8.5
* cexprtk 0.4.1

The full list of used libraries is in [requirements.txt](requirements.txt)

```Python
pip install -r requirements.txt
```

## Run from sources

To run the bot, you need to specify Telegram Bot API Token — [Get token](https://t.me/BotFather "Telegram BotFather")

The [get_token.py](src/crc-bot/common/get_token.py) script allows you to get Telegram Bot API token from .txt file when the bot is running locally or from environment variables when you want to deploy the bot.

### Run locally

1. Create an env folder with the "tg_token.txt" file in the directory from which you will run the main.py and add to file your Telegram Bot API token
2. Install all libraries from [requirements.txt](requirements.txt)
3. Run the main script — [main.py](src/crc-bot/main.py) from src/crc-bot directory

P.S. Bot token and database are hidden in [.gitignore](.gitignore)

```gitignore
# ignore secret config
bot_token.txt
db.sqlite
```

### Deploy

The project is deployed via [Railway](https://railway.app/ "Deploy to the cloud"). You can use any other cloud service or hosting, but if you want to use Railway, you need to:

1. Set up automatic deployments by specifying the required branch of your project in Railway
2. Specify path to the entry point (main.py) in Railway
3. List all libraries in [requirements.txt](requirements.txt)
4. Specify Python version in [runtime.txt](runtime.txt)
5. Specify your Telegram Bot API in Railway variables

## Modules

### src/crc-bot

* [main.py](src/crc-bot/main.py) — the main script that runs a bot polling, a scheduler for updating exchange rates and includes message handlers from all other modules through the router
* [menu.py](src/crc-bot/menu.py) — menu markup generation
* [db.py](src/crc-bot/db.py) — creating a database and working with it

### src/crc-bot/common

* [get_token.py](src/crc-bot/common/get_token.py) — getting Telegram Bot API token from environment variables (for deploy) or .txt files (for local run)
* [bot.py](src/crc-bot/common/bot.py) — bot instance module
* [rates.py](src/crc-bot/common/rates.py) — getting all exchange rates via async request to exchangerate-api
* [checks.py](src/crc-bot/common/checks.py) — methods and variables that are often used in other modules for checking different things
* [currencies.py](src/crc-bot/common/currencies.py) — all currencies supported by exchangerate-api with emoji flags

### src/crc-bot/handlers

* [round.py](src/crc-bot/handlers/round.py) — **Round** menu button handler
* [set_currencies.py](src/crc-bot/handlers/set_currencies.py) — **From/To** menu buttons handler and generation of inline currency buttons
* [rate.py](src/crc-bot/handlers/rate.py) — **Rate** menu button handler
* [converter](src/crc-bot/handlers/converter.py) — **converter** handler, conversion with built-in calculation function

### src/crc-bot/commands

* [start.py](src/crc-bot/commands/start.py) — start command handler
* [help.py](src/crc-bot/commands/help.py) — help command handler
* [about.py](src/crc-bot/commands/about.py) — about command handler and inline link-buttons
* [curr_commands.py](src/crc-bot/commands/curr_commands.py) — currency commands (/from /to /pair /swap)
