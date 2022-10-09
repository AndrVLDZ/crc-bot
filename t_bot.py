from os import remove
from turtle import back
import telebot
from telebot import types
from dataclasses import dataclass
import requests
import qiwi_tkn
import tg_tkn

@dataclass(frozen=True)
class data:
    # currency codes
    RUB: str = '643' 
    USD: str = '840' 
    EUR: str = '978' 
    KZT: str = '398'
    ОКВ: str = '156'

# currency pair exchange rate
def exchange(currency_to: str, currency_from: str): 
    s = requests.Session()
    s.headers = {'content-type': 'application/json'}
    s.headers['authorization'] = 'Bearer ' + qiwi_tkn.api_access_token
    s.headers['User-Agent'] = 'Android v3.2.0 MKT'
    s.headers['Accept'] = 'application/json'
    res = s.get('https://edge.qiwi.com/sinap/crossRates')

    # all exchange rates
    rates = res.json()['result']
    
    # requested exchange rate
    rate = [x for x in rates if x['from'] == currency_from and x['to'] == currency_to]
    if (len(rate) == 0):
        print('No rate for this currencies!')
        return
    else:
        return str(rate[0]['rate'])
        

def converter(currency_from: str,  currency_to: str, value: float, round_res: bool = True) -> list:
    exch: float = float(exchange(currency_from, currency_to))
    if round_res:
        res = [exch, round(value*exch, 2)]
    else:
        res = [exch, value*exch, 2]
    return res

# bot instance
bot = telebot.TeleBot(tg_tkn.bot_access_token)

# /start command function
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_token = types.KeyboardButton('Добавить токен')
    remove_token = types.KeyboardButton('Удалить токен')
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
            qiwi_tkn.get()
        
        if message.text == 'Курсы валют':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            usd = types.KeyboardButton('Доллар')
            eur = types.KeyboardButton('Евро')
            kzt = types.KeyboardButton('Тенге')
            okb = types.KeyboardButton('Юань')
            back = types.KeyboardButton('Назад')
            markup.add(usd, eur, kzt, okb, back)
            bot.send_message(message.chat.id, 'Выбери валюту', reply_markup=markup)

        if message.text == 'Доллар':
                currency_from: str = data.USD
                currency_to: str = data.RUB
                answ: float = exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, f'Текущий курс: {answ}')
        
        elif message.text == 'Евро':
                currency_from: str = data.EUR
                currency_to: str = data.RUB
                answ: float = exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, f'Текущий курс: {answ}')
        
        elif message.text == 'Тенге':
                currency_from: str = data.KZT
                currency_to: str = data.RUB
                answ: float = exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, f'Текущий курс: {answ}')
        
        elif message.text == 'Юань':
                currency_from: str = data.ОКВ
                currency_to: str = data.RUB
                answ: float = exchange(currency_from, currency_to)
                bot.send_message(message.chat.id, f'Текущий курс: {answ}')

while True:
    try:
      bot.polling(none_stop=True)
    except: 
      print('error')
      logging.error('error: {}'.format(sys.exc_info()[0]))
      time.sleep(5)