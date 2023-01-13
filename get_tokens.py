import logging
from os import environ

logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


# reading a token from .txt file
def get_from_txt(file_name: str) -> str:
    try:
        f = open(file_name, "r")
    except:
        raise FileNotFoundError(f"{file_name} not found!")
    token = f.read()
    if token != "":
        return token
    raise ValueError(f"Token not found in {file_name}!")


# getting Telegram Bot API and QIWI API tokens
def get_secrets() -> tuple[str, str]:
  bot_token = environ.get('BOT_TOKEN')
  qiwi_token = environ.get('QIWI_TOKEN')
  
  if qiwi_token and bot_token:
    # both environment variables exist, return them as a tuple
    logging.info("Tokens were obtained from environment variables")
    return (bot_token, qiwi_token)
  
  if not qiwi_token:
    logging.info("QIWI_TOKEN does not exist in the environment variables")

  if not bot_token:
    logging.info("BOT_TOKEN does not exist in the environment variables")
  
  logging.info("Trying to read tokens from files...")
  bot_token = get_from_txt("bot_token.txt")
  qiwi_token = get_from_txt("qiwi_token.txt")
  logging.info("Tokens were obtained from .txt files")
  return (bot_token, qiwi_token)
