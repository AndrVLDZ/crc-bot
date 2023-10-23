# CRC Bot

![info picture](/CRC_git.png)3.1.0

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

* python 3.11.4
* aiogram 3.1.0
* aiosqlite 0.19.0
* aiohttp 3.8.5
* cexprtk 0.4.1

The full list of used libraries is in [requirements.txt](requirements.txt)

```Python
pip install -r requirements.txt
```

## Run from sources

To run the bot, you need to specify Telegram Bot API Token — [Get token](https://t.me/BotFather "Telegram BotFather")

The get_token.py script allows you to get tokens from .txt file or environment variables. This script is written to get tokens from .txt files when the bot is running locally or from environment variables when you want to deploy the bot.

### Run locally

1. Create tg_token.txt and add to file your telegram bot API token
2. Install all libraries from [requirements.txt](requirements.txt)
3. Run the main script — [bot.py](bot.py)

P.S. Bot token and database are hidden in [.gitignore](.gitignore)

```gitignore
# ignore secret config
bot_token.txt
db.sqlite
```

### Deploy

The project is deployed via [Railway](https://railway.app/ "Deploy to the cloud"). You can use any other cloud service or hosting, but if you want to use Railway, you need to:

1. Set up automatic deployments by specifying the required branch of your project in Railway
2. Specify the entry point (main.py) in Railway
3. List all libraries in [requirements.txt](requirements.txt)
4. Specify Python version in [runtime.txt](runtime.txt)
5. Specify your Telegram Bot API in Railway variables

## Modules

* [main.py](main.py) — bot instance module
* [bot.py](bot.py) — the main script that runs a bot polling, a scheduler for updating exchange rates and includes message handlers from all other modules through the router
* [get_token.py](get_token.py) — getting Telegram Bot API and QIWI API tokens from environment variables (for deploy) or .txt files (for local run)
* [db.py](db.py) — creating a database and working with it
* [rates.py](rates.py) — getting all exchange rates via async request to exchangerate-api
* [menu.py](menu.py) — menu markup generation
* [common.py](common.py) — methods and variables that are often used in different modules
* [start.py](commands/start.py) — start command handler
* [help.py](commands/help.py) — help command handler
* [about.py](commands/about.py) — about command handler and inline link-buttons
* [curr_commands.py](commands/curr_commands.py) — currency commands (/from /to /pair /swap)
* [round.py](handlers/round.py) — **Round** menu button handler
* [set_currencies.py](handlers/set_currencies.py) — **From/To** menu buttons handler and generation of inline currency buttons
* [rate.py](handlers/rate.py) — **Rate** menu button handler
* [converter](handlers/converter.py) — **converter** handler, conversion with built-in calculation function
