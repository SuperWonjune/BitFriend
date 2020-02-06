import telegram
from telegram.ext import Updater, CommandHandler


BOT_TOKEN = '1040424564:AAF9a6nwmsD7_0Dzuow4bpkexfUSiP2PQ7o'
chat_id = '996769937'
bot_name = 'wonjune_bot'

class TelegramBot:
    def __init__(self, name, token):
        self.core = telegram.Bot(token)
        self.updater = Updater(token=token, use_context=True)
        self.id = chat_id
        self.name = name

    def sendMessage(self, text):
        self.core.sendMessage(chat_id = self.id, text=text)

    def stop(self):
        self.updater.start_polling()
        self.updater.dispatcher.stop()
        self.updater.job_queue.stop()
        self.updater.stop()


class User_Bot(TelegramBot):
    def __init__(self):
        self.token = BOT_TOKEN
        TelegramBot.__init__(self, bot_name, self.token)
        self.updater.stop()

    def add_handler(self, cmd, func):
        self.updater.dispatcher.add_handler(CommandHandler(cmd, func))

    def start(self):
        self.sendMessage('안녕! 만나서 반가워!')
        self.updater.start_polling()