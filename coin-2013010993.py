import requests
import json
import csv
import datetime
import os.path
import time
from pprint import pprint
from collections import deque

import telepot
from telepot.loop import MessageLoop
from apscheduler.schedulers.background import BackgroundScheduler


def get_coin_info_and_send():
    my_id = 635214368
    csv_file_name = 'more price.csv'
    # Get BTC / USD from cryptocompare
    # fsym : From Symbol
    # tyms : To Symbols, include multiple symbols
    symbol_query = {'fsym': 'BTC', 'tsyms': 'USD'}
    crypto_request = requests.get('https://min-api.cryptocompare.com/data/price',
                                  params=symbol_query)
    parsed_data_crp = json.loads(crypto_request.text)
    # get current BTC in USD
    btc_in_usd = parsed_data_crp.get('USD')

    # Get BTC / KRW from bithumb
    bithumb_request = requests.get('https://api.bithumb.com/public/ticker/BTC')
    parsed_data_bitb = json.loads(bithumb_request.text)
    # get current BTC in KRW
    btc_in_krw = parsed_data_bitb['data']['sell_price']

    # get previous coin datas from csv to compare UP and DOWN
    file_exists = os.path.isfile(csv_file_name)
    if file_exists:
        with open(csv_file_name, 'r') as file:
            lastrow = deque(csv.reader(file), 1)[0]
            changed_USD = round(btc_in_usd - float(lastrow[1]), 2)
            changed_KRW = int(btc_in_krw) - int(lastrow[2])

    # store new datas in csv
    with open(csv_file_name, 'a') as file:
        fieldnames = ['Date', 'Bitfinex-BTC-USD', 'Bithumb-BTC-KRW']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        now = datetime.datetime.now()
        writer.writerow({'Date': now.strftime('%Y-%m-%d %H:%M'),
                         'Bitfinex-BTC-USD': btc_in_usd,
                         'Bithumb-BTC-KRW': btc_in_krw})

    # set differences between prices
    updown_message_KRW = 'UP' if changed_KRW >= 0 else 'DOWN'
    updown_message_USD = 'UP' if changed_USD >= 0 else 'DOWN'
    send_message = 'BTC IN KRW : ' + str(btc_in_krw) + \
                   ' ₩, ' + updown_message_KRW + ' ' + str(changed_KRW) + '\n'\
                   + 'BTC IN USD : ' + str(btc_in_usd) + \
                   ' $, ' + updown_message_USD + ' ' + str(changed_USD)

    # send a message
    bot.sendMessage(my_id, send_message)
    print('Message sent to', my_id, '\n' + send_message)


def handle(msg):
    # show data of user with iput
    pprint(msg)
    # handle input messages
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        bot.sendMessage(chat_id, 'LEAVE ME ALONE')


def load_on_scheduler(func, interval_sec):
    print('Loading on scheduler...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(func, 'interval', seconds=interval_sec)
    scheduler.start()


# Function start at here
if __name__ == "__main__":
    # bot TOKENS
    TOKENS = '626282775:AAGSZOkZw7n1EzVX09VF15JvCHvig9y3GNs'
    # connect to a bot
    print('Connecting To Bot...')
    bot = telepot.Bot(TOKENS)
    MessageLoop(bot, handle).run_as_thread()

    # load on awscheduler
    load_on_scheduler(get_coin_info_and_send, 60)

    print("ctrl + c to exit")
    while True:
        time.sleep(10)

