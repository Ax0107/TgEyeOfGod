"""

Main Script to run app

"""

from config import APP_ID, API_KEY, USERNAME, PHONE
import asyncio

import json
from logger import logger
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerChannel, InputMessagesFilterPhotos
import time

logger = logger('MAIN')


class Client(object):

    def __init__(self):

        # Создаём клиент и авторизуемся
        self.client = TelegramClient(USERNAME, APP_ID, API_KEY)

    async def auth(self):
        await self.client.connect()
        logger.info("Клиент запущен.")
        # Проверяем, точно ли мы авторизованы
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(PHONE)
            try:
                logger.warning("Включена двух-факторная авторизация. Необходимо ввести код.")
                await self.client.sign_in(PHONE, input('Введите код: '))
            except SessionPasswordNeededError:
                logger.warning("Ошибка. Необходимо ввести пароль.")
                await self.client.sign_in(password=input('Введите пароль: '))
        return True


async def main():
    client = Client()
    if not await client.auth():
        logger.error('Невозможно авторизоваться.')
        return

    CHAT_ID = 'durovschat'

    photos = await client.client.get_messages(CHAT_ID, 0, filter=InputMessagesFilterPhotos)
    print(photos.total)


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  loop.close()


