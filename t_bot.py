import traceback
import telebot
from telebot import types
from dataclasses import dataclass
import get_tkn
import get_tkn
import qiwi_tools

# default currency
currency_to = qiwi_tools.data.RUB

# bot instance
token = get_tkn.get('tg_token.txt')
bot = telebot.TeleBot(token)

# /start command function
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_token = types.KeyboardButton('Добавить токен')
    converter = types.KeyboardButton('Конвертация')
    exchange = types.KeyboardButton('Курсы валют')
    
    markup.add(add_token, exchange)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))
    bot.send_message(message.chat.id, 'Я бот для мониторинга валютных курсов QIWI и быстрой конвертации')
    bot.send_message(message.chat.id, 'Для работы мне понадобится токен твоего QIWI кошелька. \nДля этого нажми на [добавить токен] в меню. \nТокен можно удалить через [меню]\n___________________\n[бот в разработке]', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Добавить токен':
            get_tkn.get()
        
        elif message.text == 'Курсы валют':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            usd = types.KeyboardButton('Доллар')
            eur = types.KeyboardButton('Евро')
            kzt = types.KeyboardButton('Тенге')
            okb = types.KeyboardButton('Юань')
            back = types.KeyboardButton('Назад')
            markup.add(usd, eur, kzt, okb, back)
            bot.send_message(message.chat.id, 'Выбери валюту', reply_markup=markup)

        # elif message.text == 'Назад':
        #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        #     remove_token = types.KeyboardButton('Удалить токен')
        #     converter = types.KeyboardButton('Конвертация')
        #     exchange = types.KeyboardButton('Курсы валют')
            
        #     markup.add(remove_token, exchange)
        #     bot.send_message(message.chat.id, 'Главное меню')

        elif message.text == 'Доллар':
                currency_from: str = qiwi_tools.data.USD
                answ: float = qiwi_tools.exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, answ)
        
        elif message.text == 'Евро':
                currency_from: str = qiwi_tools.data.EUR
                answ: float = qiwi_tools.exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, answ)
        
        elif message.text == 'Тенге':
                currency_from: str = qiwi_tools.data.KZT
                answ: float = qiwi_tools.exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, answ)
        
        elif message.text == 'Юань':
                currency_from: str = qiwi_tools.data.ОКВ
                answ: float = qiwi_tools.exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, answ)

while True:
    try:
      bot.polling(none_stop=True)
    except Exception as e:
        print('Ошибка:\n', traceback.format_exc())