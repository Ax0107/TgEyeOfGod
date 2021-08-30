"""

Main Script to run app

"""

import asyncio
import json

from telethon import events
from client import Client
from config import SPEC_REQUEST_PREFIX, SPEC_REQUEST_PREFIX_click, SPEQ_REQUEST_SPLITER
from logger import logger
logger = logger('MAIN')

OUR_BOT_ID = 'g_eye_bot'
OUR_BOT_ID_num = 1881360516
EYE_OF_GOD_BOT_ID = 'pguzod36198bot'  # ТЕСТОВЫЙ БОТ
EYE_OF_GOD_BOT_ID_num = 1866519260  # ТЕСТОВЫЙ БОТ


users_queue = []
last_user = ''

client = Client()

messages_queue = {}


async def message_handler(event):
    global last_user
    try:
        message = event.message

        # Приходит сообщение от юзера в бота, бот отправляет этот запрос нашему клиенту
        if message.peer_id.user_id == OUR_BOT_ID_num:
            """ 
              Отправка запроса на клиент
                        \
            [*]          - Отправка клиентом сообщения Глазу Бога
                                    \
                                        ...
            [*] - Текущее состояние
    
            """

            if message.text[:len(SPEC_REQUEST_PREFIX)] == SPEC_REQUEST_PREFIX:
                await handle_message_request(message)
            elif message.text[:len(SPEC_REQUEST_PREFIX_click)] == SPEC_REQUEST_PREFIX_click:
                await handle_button_click_request(message)

            else:
                logger.debug('Не сообщение-запрос. Игрорирую.')
                return

        # Ждём ответ от глаза бога

        elif message.peer_id.user_id == EYE_OF_GOD_BOT_ID_num:
            """ 
                    ...
                                    \
            [*]                      - Получение ответа от ГБ клиентом
                                                \
            [*]                                  - Пересылка сообщения боту с помощью клиента
                                                            \
            [*]  - - - - - - - - - - - - - - - - - - - -     - Пересылка сообщения ботом пользователю
            
            
            [*] - Текущее состояние
    
            """

            logger.info('ПОЛУЧЕН ОТВЕТ ОТ ГЛАЗА БОГА. Пересылаю ответ через бота юзеру.')
            try:
                # Получаем последнего юзера в очереди
                try:
                    to_peer = users_queue.pop()
                except:
                    to_peer = last_user

                last_user = to_peer
                path = ''
                if message.document:
                    path = await message.download_media()

                reply_markup = ''
                if message.reply_markup:
                    reply_markup = message.reply_markup.to_json()

                messages_queue[to_peer] = message

                # Нашему боту отправляем сообщение вида "Кому:Что ответил глаз:кнопки"
                await client.client.send_message(OUR_BOT_ID, f"{to_peer}{SPEQ_REQUEST_SPLITER}{message.text}{SPEQ_REQUEST_SPLITER}{reply_markup}{SPEQ_REQUEST_SPLITER}{path}")
            except Exception as e:
                logger.error(e)

        else:
            # logger.debug('Другой чат. Игнорирую сообщение.')
            logger.info(f'Другой чат. Игнорирую сообщение: {message.from_id.user_id} {message}')
            return
        logger.debug('ok')
    except Exception as e:
        logger.error(f'E: {e}')


async def handle_message_request(message):
    global last_user
    # Обрезаем спец.префикс запроса
    message.text = message.text[len(SPEC_REQUEST_PREFIX):]

    logger.info('ПОЛУЧЕН НОВЫЙ ЗАПРОС. Пересылаю ответ через бота Глазу бога.')

    to_peer = message.text.split(SPEQ_REQUEST_SPLITER)[0]
    last_user = to_peer
    text = message.text.replace(to_peer, '').replace(SPEQ_REQUEST_SPLITER, '')
    users_queue.append(to_peer)

    try:
        # Отправляем запрос глазу бога
        await client.client.send_message(EYE_OF_GOD_BOT_ID, f"{text}")
    except Exception as e:
        logger.error(e)


async def handle_button_click_request(message):
    # Обрезаем спец.префикс запроса
    message.text = message.text[len(SPEC_REQUEST_PREFIX_click):]
    logger.info('ПОЛУЧЕН НОВЫЙ ЗАПРОС (клик по кнопке). Нажимаю кнопку в боте Глаза бога.')

    to_peer = message.text.split(SPEQ_REQUEST_SPLITER)[0]
    callback_data = message.text.replace(to_peer, '').replace(SPEQ_REQUEST_SPLITER, '')
    users_queue.append(to_peer)

    try:
        # Отправляем запрос глазу бога
        row, col = map(int, callback_data.split('-'))
        logger.info(f'Clicking on {row} {col}')
        logger.info(dir(message))
        logger.debug(message)
        message_to_answer = messages_queue[to_peer]
        await message_to_answer.click(row, col)
    except Exception as e:
        logger.error(e)


@client.client.on(events.MessageEdited)
async def handler(event):
    global last_user
    users_queue.append(last_user)
    await message_handler(event)


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


