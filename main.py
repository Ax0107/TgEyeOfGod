"""

Main Script to run app

"""

import asyncio

from telethon import events
from client import Client

from logger import logger
logger = logger('MAIN')

OUR_BOT_ID = 'g_eye_bot'
OUR_BOT_ID_num = 1881360516
EYE_OF_GOD_BOT_ID = 'ge_second_test_bot'  # ТЕСТОВЫЙ БОТ
EYE_OF_GOD_BOT_ID_num = 1913374406  # ТЕСТОВЫЙ БОТ


users_queue = []
last_user = 'g_eye_bot'

client = Client()


async def eye_god_message_handler(event):
    logger.debug(f'Callback called.')
    # logger.info(event)
    # logger.info(dir(event))
    message = event.message.to_dict()
    if event.chat_id == EYE_OF_GOD_BOT_ID_num:
        logger.info('ПОЛУЧЕН ОТВЕТ ОТ ГЛАЗА БОГА. Пересылаю ответ через бота юзеру.')

        await client.client.send_message(OUR_BOT_ID, f"{message.from_user.id}:{message.text}")

    elif event.chat_id == OUR_BOT_ID_num:
        logger.info('ПОЛУЧЕН НОВЫЙ ЗАПРОС. Пересылаю ответ через бота Глазу бога.')

        await client.client.send_message(EYE_OF_GOD_BOT_ID, f"{message.from_user.id}:{message.text}")
    logger.info('ok')


async def main():

    if not await client.auth():
        logger.error('Невозможно авторизоваться.')
        return

    client.client.add_event_handler(eye_god_message_handler, events.NewMessage)
    await client.client.run_until_disconnected()


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()


