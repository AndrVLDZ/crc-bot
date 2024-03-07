from common.logs import log
from os import environ
from typing import Union

BOT_TKN_FILE = "env/bot_token.txt"


# reading a token from .txt file
def get_from_txt(file_name: str) -> Union[str, bool]:
    token: str = ""
    try:
        with open(file_name, "r") as f:
          token = f.read()
    except:
        log.info(f"{file_name} not found!")
        return False
    if token != "":
        return token
    log.info(f"Token not found in {file_name}!")
    return False


# getting Telegram Bot API token
def get_secrets() -> tuple[str, str]:
  bot_token = environ.get('BOT_TOKEN')

  if bot_token:
    # both environment variables exist, return them as a tuple
    log.info("Tokens were obtained from environment variables")
    return (bot_token)

  if not bot_token:
    log.info("BOT_TOKEN does not exist in the environment variables")

  log.info("Trying to read token from file...")

  bot_token = get_from_txt(BOT_TKN_FILE)
  if bot_token:
    log.info("Bot token was obtained from .txt file")
    return (bot_token)

  return False
