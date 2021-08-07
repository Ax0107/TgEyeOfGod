"""

Main Script to run app

"""

import asyncio
from telethon.tl.types import InputMessagesFilterPhotos

from client import Client

from logger import logger
logger = logger('MAIN')


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


