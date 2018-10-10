import requests
import json
from pprint import pprint
import telepot
from telepot.loop import MessageLoop

from apscheduler.schedulers.background import BlockingScheduler


def get_coin_info():
    # Get BTC / USD from cryptocompare
    # fsym : From Symbol
    # tyms : To Symbols, include multiple symbols
    symbol_query = {'fsym': 'BTC', 'tsyms': 'USD'}
    crypto_request = requests.get('https://min-api.cryptocompare.com/data/price', params=symbol_query)
    parsed_data_crp = json.loads(crypto_request.text)

    # current BTC in USD
    btc_in_usd = parsed_data_crp.get('USD')
    print(btc_in_usd)

    # Get BTC / KRW from bithumb
    bithumb_request = requests.get('https://api.bithumb.com/public/ticker/BTC')
    parsed_data_bitb = json.loads(bithumb_request.text)

    # current BTC in KRW
    btc_in_krw = parsed_data_bitb['data']['sell_price']
    print(btc_in_krw)

    send_message = 'BTC IN KRW : ' + str(btc_in_krw) + ' ₩\n' + 'BTC IN USD : ' + str(btc_in_usd) + ' $'

    bot.sendMessage(336890005, send_message)
    # bot.sendMessage(336890005, 'BTC IN USD : ' + str(btc_in_usd) + ' $')
    bot.sendMessage(635214368, send_message)
    # bot.sendMessage(635214368, 'BTC IN USD : ' + str(btc_in_usd) + ' $')


def handle(msg):
    # show data of user with iput
    pprint(msg)

    # handle input messages
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        bot.sendMessage(chat_id, 'NO, YOU ' + msg['text'] + '!')


# create bot
bot = telepot.Bot('626282775:AAGSZOkZw7n1EzVX09VF15JvCHvig9y3GNs')
MessageLoop(bot, handle).run_as_thread()

# load on awscheduler
scheduler = BlockingScheduler()
scheduler.add_job(get_coin_info, 'interval', seconds=20)
scheduler.start()
