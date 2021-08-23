"""

Main Script to run app

"""

import asyncio

from telethon import events
from client import Client
from config import SPEC_REQUEST_PREFIX
from logger import logger
logger = logger('MAIN')

OUR_BOT_ID = 'g_eye_bot'
OUR_BOT_ID_num = 1881360516
EYE_OF_GOD_BOT_ID = 'ge_second_test_bot'  # ТЕСТОВЫЙ БОТ
EYE_OF_GOD_BOT_ID_num = 1913374406  # ТЕСТОВЫЙ БОТ


users_queue = []
last_user = 'g_eye_bot'

client = Client()


async def message_handler(event):
    logger.debug(f'Callback called: {event.message.chat_id} {event.message.text}')

    message = event.message

    # Приходит сообщение от юзера в бота, бот отправляет этот запрос нашему клиенту

    if message.from_id.user_id == OUR_BOT_ID_num:
        """ 
          Отправка запроса на клиент
                    \
        [*]          - Отправка клиентом сообщения Глазу Бога
                                \
                                 - Получение ответа от ГБ клиентом
                                            \
                                             - Пересылка сообщения боту с помощью клиента
                                                        \
                                                         - Пересылка сообщения ботом пользователю
        [*] - Текущее состояние

        """

        # Бот отправляет нам информацию ввиде "__USER_ID:REQUEST",
        # Получаем юзера и добавляем его в очередь обработки

        if message.text[:len(SPEC_REQUEST_PREFIX)] != SPEC_REQUEST_PREFIX:
            logger.debug('Не сообщение-запрос. Игрорирую.')
            return
        # Обрезаем спец.префикс запроса
        message.text = message.text[len(SPEC_REQUEST_PREFIX):]

        logger.info('ПОЛУЧЕН НОВЫЙ ЗАПРОС. Пересылаю ответ через бота Глазу бога.')

        to_peer = message.text.split(':')[0]
        text = message.text.replace(to_peer, '')[1:]
        users_queue.append(to_peer)

        try:
            # Отправляем запрос глазу бога
            await client.client.send_message(EYE_OF_GOD_BOT_ID, f"{text}")
        except Exception as e:
            logger.error(e)

    # Ждём ответ от глаза бога

    elif message.from_id.user_id == EYE_OF_GOD_BOT_ID_num:
        """ 
          Отправка запроса на клиент
                    \
                     - Отправка клиентом сообщения Глазу Бога
                                \
        [*]                      - Получение ответа от ГБ клиентом
                                            \
        [*]                                  - Пересылка сообщения боту с помощью клиента
                                                        \
        [*]                                              - Пересылка сообщения ботом пользователю
        
        
        [*] - Текущее состояние

        """

        logger.info('ПОЛУЧЕН ОТВЕТ ОТ ГЛАЗА БОГА. Пересылаю ответ через бота юзеру.')

        # Получаем последнего юзера в очереди
        to_peer = users_queue.pop()

        try:
            # Нашему боту отправляем сообщение вида "Кому:Что ответил глаз"
            await client.client.send_message(OUR_BOT_ID, f"{to_peer}:{message.text}")
        except Exception as e:
            logger.error(e)

    else:
        logger.debug('Другой чат. Игнорирую сообщение.')
        return
    logger.debug('ok')


async def main():

    if not await client.auth():
        logger.error('Невозможно авторизоваться.')
        return

    client.client.add_event_handler(message_handler, events.NewMessage)
    await client.client.run_until_disconnected()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()


