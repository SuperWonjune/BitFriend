import ChatBotModel

def proc_joke(update, context):
    update.message.reply_text('반성문을 영어로 하면?')
    update.message.reply_text('글로벌')

def proc_stop(update, context):
    update.message.reply_text('안녕 잘 지내!')


print('프로그램이 실행중입니다... ctrl+c를 눌러서 종료해주세요!')
chat_bot = ChatBotModel.User_Bot()
chat_bot.add_handler('joke', proc_joke)
chat_bot.add_handler('stop', proc_stop)
chat_bot.start()