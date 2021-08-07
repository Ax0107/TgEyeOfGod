"""

Main Script to run app

"""

import asyncio

from telethon import events
from client import Client

from logger import logger
logger = logger('MAIN')

OUR_BOT_ID = 'g_eye_bot'
OUR_BOT_ID = 'g_eye_bot'
EYE_OF_GOD_BOT_ID = 'ge_second_test_bot'  # ТЕСТОВЫЙ БОТ
EYE_OF_GOD_BOT_ID_num = 1913374406  # ТЕСТОВЫЙ БОТ


async def eye_god_message_handler(event):
    logger.debug('Callback called.')
    # logger.info(event)
    # logger.info(dir(event))
    if event.chat_id == EYE_OF_GOD_BOT_ID_num:
        logger.info('ПОЛУЧЕН ОТВЕТ ОТ ГЛАЗА БОГА.')


async def main():
    client = Client()
    if not await client.auth():
        logger.error('Невозможно авторизоваться.')
        return

    # messages = await client.client.get_messages(CHAT_ID, 0)
    # print(messages.total)

    client.client.add_event_handler(eye_god_message_handler, events.NewMessage)
    await client.client.run_until_disconnected()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()


