"""

Файл для работы бота

"""

import telebot
from config import BOT_TOKEN, SPEC_REQUEST_PREFIX
from messages import MESSAGES, Keyboards
from sqlalchemy.exc import NoResultFound
from database import session, User, register_user

from logger import logger
logger = logger('BOT')

bot = telebot.TeleBot(BOT_TOKEN)

CLIENT_ID = 270994676


@bot.message_handler(commands=['start'])
def start_command(message):
    logger.info('Got new "start" command-message.')
    try:
        obj = session.query(User).filter_by(telegram_id=message.chat.id).one()
        print('USER FOUND:', obj.phone)
        # TODO: Handle this situation
    except NoResultFound:
        logger.info('New user. Starting registration.')

        bot.send_message(message.chat.id, MESSAGES['/start'], reply_markup=Keyboards.phone_keyboard())
        bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=handle_first_step_registration)


@bot.message_handler(content_types=['contact'])
def handle_first_step_registration(message):
    if message.contact is not None:
        logger.debug(message.contact)
        register_user(telegram_id=message.chat.id, name=message.contact.first_name, phone=message.contact.phone_number,
                      current_state='main')

        bot.send_message(message.chat.id, MESSAGES['successful_registration'])

        return handle_main_state(message)


def handle_main_state(message):
    obj = session.query(User).filter_by(telegram_id=message.chat.id).one()
    bot.send_message(message.chat.id, MESSAGES['MAIN_STATE'].format(reg_dt=obj.registration_datetime,
                                                                    money_count=obj.money_count,
                                                                    subs_due=obj.subscribe_due))





#
# @bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id == CLIENT_ID and False)
# def handle_response(response_message):
#     # Получение и отправка ответа пользователю
#     data = response_message.text.split(':')
#     try:
#         text = ':'.join(data[1:])
#         user_id = data[0]
#
#         bot.send_message(user_id, text)
#     except Exception as e:
#         logger.error(e)
#         handle_message(response_message)
#
#
# @bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id != CLIENT_ID)
# def handle_message(message):
#     logger.info(message.from_user.id)
#     # Отправка сообщения-запроса на клиент
#     bot.send_message(CLIENT_ID, f"{SPEC_REQUEST_PREFIX}{message.from_user.id}:{message.text}")


if __name__ == "__main__":
    bot.polling(none_stop=True)




