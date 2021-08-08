"""

ФАЙЛ ТЕСТИРОВАНИЯ РАБОТЫ С БОТОМ (ВМЕСТО ЭТОГО БОТА БУДЕТ ВЫСТУПАТЬ БОТ-ГЛАЗ-БОГА)


"""

import telebot
from config import SECOND_BOT_TOKEN
from time import sleep


from logger import logger
logger = logger('BOT')

bot = telebot.TeleBot(SECOND_BOT_TOKEN)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    logger.info(message.text)
    sleep(6)
    bot.send_message(message.from_user.id, f"Вот информация по запросу: {message.text}\n\nХАХАХАХ")


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)




