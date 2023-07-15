from aiogram import Bot

from get_token import get_secrets

bot_token = get_secrets()
bot = Bot(token=bot_token)
