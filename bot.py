"""

Файл для работы бота

"""

import telebot
from config import BOT_TOKEN, SPEC_REQUEST_PREFIX
from logger import logger
logger = logger('BOT')

bot = telebot.TeleBot(BOT_TOKEN)

CLIENT_ID = 270994676


@bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id == CLIENT_ID)
def handle_response(response_message):
    # Получение и отправка ответа пользователю
    data = response_message.text.split(':')
    try:
        text = ':'.join(data[1:])
        user_id = data[0]

        bot.send_message(user_id, text)
    except Exception as e:
        logger.error(e)
        handle_message(response_message)


@bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id != CLIENT_ID)
def handle_message(message):
    logger.info(message.from_user.id)
    # Отправка сообщения-запроса на клиент
    bot.send_message(CLIENT_ID, f"{SPEC_REQUEST_PREFIX}{message.from_user.id}:{message.text}")



if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)




