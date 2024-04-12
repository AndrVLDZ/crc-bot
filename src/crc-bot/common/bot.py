from aiogram import Bot
from dotenv import load_dotenv
import os

env_path =  os.path.join(os.getcwd(), ".env")
load_dotenv(env_path)


def get_bot() -> Bot | None:
    bot_token = os.getenv("BOT_TOKEN")
    if bot_token:
        bot = Bot(token=bot_token)
        return bot


if __name__ == "__main__":
    pass
else:
    bot = get_bot()
