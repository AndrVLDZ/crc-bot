# Travel_CRC_bot

<!-- ![info picture](/CRC_Description_git.png)   -->

## About  

Financial Telegram bot for travel. Set your currency and the currency of the country and translate prices in stores into understandable and familiar values with a currency converter and a built-in calculator.

See running bot: [@Travel_CRC_bot](https://t.me/Travel_CRC_bot "Travel Converter Rate Calculator")

## Features

* Setting the currency pair and rounding mode
* Solving a user-sent mathematical expressions before converting
* Converting a value sent via message or the result of a user-sent math expression
* Sending the exchange rate of the selected currency pair
* Saving user settings (currency pair and rounding mode)

## Dependencies  

* Python 3.10.8
* Aiogram 3.0.0b6
* asyncio-periodic 2019.2
* cexprtk 0.4.0

P.S. The full list of used libraries is in [requirements.txt](requirements.txt)

## Run from sources  

To run the bot, you need to specify two tokens:

* Telegram Bot API Token — [Get token](https://t.me/BotFather "Telegram BotFather")
* QIWI API Token — [Get token](https://qiwi.com/api "QIWI API")

The get_tokens.py script allows you to get tokens from .txt files or environment variables. This script is written to get tokens from .txt files when the bot is running locally or from environment variables when you want to deploy the bot.

### Run locally  

1. Create qiwi_token.txt and add to file your QIWI API token  
2. Create tg_token.txt and add to file your telegram bot API token  
3. Install all libraries from [requirements.txt](requirements.txt)  
4. Run the main script — [bot.py](bot.py)  

P.S. All tokens and database are hidden in [.gitignore](.gitignore)

``` gitignore
# ignore secret config
bot_token.txt
qiwi_token.txt
bot.sqlite
```

### Deploy  

The project is deployed via [Railway](https://railway.app/ "Deploy to the cloud"). You can use any other cloud service or hosting, but if you want to use Railway, you need to:  

1. Specify the entry point (bot.py) in the [Procfile](Procfile)  
2. List all libraries in [requirements.txt](requirements.txt)  
3. Specify Python version in [runtime.txt](runtime.txt)
4. Specify your Telegram Bot API and QIWI API tokens in Railway variables
5. Set up automatic deployments by specifying the required branch of your project in Railway

## Modules  

* [bot](bot.py) — the main script that runs a bot polling, a scheduler for updating exchange rates and includes message handlers from all other modules through the router  
* [get_tokens](get_tokens.py) — getting Telegram Bot API and QIWI API tokens from environment variables (for deploy) or .txt files (for local run)  
* [db](db.py) — creating a database and working with it  
* [qiwi](qiwi.py) — work with QIWI API, getting rate from QIWI API answer  
* [menu](menu.py) — menu markup generation  
* [tools](tools.py) — user validation  
* [h_start](h_start.py) — start command handler  
* [h_help](h_help.py) — help command handler  
* [h_about](h_about.py) — about command handler and inline link-buttons  
* [h_round](h_round.py) — **Round** menu button handler  
* [h_set_currencies](h_set_currencies.py) — **Set currencies** menu button handler and inline buttons generation
* [h_rate](h_rate.py) — **Rate** menu button handler  
* [h_converter](h_converter.py) — **converter** handler, conversion with built-in calculation functionality  
