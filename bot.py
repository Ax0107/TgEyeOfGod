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
        return handle_message(message)
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
                                                                    subs_due=obj.subscribe_due),
                     reply_markup=Keyboards.main_keyboard())


""" ---------------------------------------------- SEARCHING --------------------------------------------------------"""


@bot.message_handler(content_types=['text'], func=lambda msg: msg.text == MESSAGES['keyboards']['MAIN']['search'])
def handle_search_state(message):
    obj = session.query(User).filter_by(telegram_id=message.chat.id).one()
    obj.set_state('search')
    bot.send_message(message.chat.id, MESSAGES['SEARCH_STATE'])
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=handle_search_state__start_search)


def handle_search_state__start_search(message):
    """
     [*] - Отправка запроса на клиент
                \
                 - Отправка клиентом сообщения Глазу Бога
                            \
                             - Получение ответа от ГБ клиентом
                                        \
                                         - Пересылка сообщения боту с помощью клиента
                                                    \
                                                     - Пересылка сообщения ботом пользователю
    [*] - Текущее состояние

    """

    bot.send_message(CLIENT_ID, f"{SPEC_REQUEST_PREFIX}{message.from_user.id}:{message.text}")
    bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=handle_end_search)

@bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id == CLIENT_ID)
def handle_response(response_message):
    """
      Отправка запроса на клиент
                \
                                ...
                                                    \
    [*]  - - - - - - - - - - - - - - - - - - - -     - Пересылка сообщения ботом пользователю

    [*] - Текущее состояние
    """

    data = response_message.text.split(':')
    try:
        text = ':'.join(data[1:])
        user_id = data[0]
        # Отправка ответа
        bot.send_message(user_id, text)
        bot.send_message(user_id, MESSAGES['end_search'], reply_markup=Keyboards.end_search())


    except Exception as e:
        logger.error(e)
        handle_message(response_message)


def handle_end_search(message):
    if message.text == MESSAGES['keyboards']['SEARCH']['go_main']:
        logger.debug('Going main...')
        return go_main(message)
    elif message.text == MESSAGES['keyboards']['SEARCH']['start_again']:
        logger.debug('Starting searching again...')
        return handle_search_state(message)
    else:
        bot.send_message(message.chat.id, MESSAGES['no_command'], reply_markup=Keyboards.end_search())
        bot.register_next_step_handler_by_chat_id(chat_id=message.chat.id, callback=handle_end_search)


@bot.message_handler(content_types=['text'], func=lambda msg: msg.from_user.id != CLIENT_ID)
def handle_message(message):
    try:
        obj = session.query(User).filter_by(telegram_id=message.chat.id).one()
    except NoResultFound:
        return start_command(message)

    state = obj.get_state()
    if state == 'main':
        return handle_main_state(message)
    elif state == 'search':
        return handle_search_state(message)


def go_main(message):
    try:
        obj = session.query(User).filter_by(telegram_id=message.chat.id).one()
    except NoResultFound:
        return start_command(message)

    obj.set_state('main')
    return handle_main_state(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
