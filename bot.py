"""

Файл для работы бота

"""

import telebot
from config import BOT_TOKEN
from logger import logger
logger = logger('BOT')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    logger.info(message.text)

    bot.send_message(message.from_user.id, "Да, я получил твоё сообщение.")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)




