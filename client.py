"""

Файл клиента telegram

"""

from config import APP_ID, API_KEY, USERNAME, PHONE

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from logger import logger
logger = logger('TG-CLIENT')


class Client(object):

    def __init__(self):
        # Создаём клиент
        self.client = TelegramClient(USERNAME, APP_ID, API_KEY)

    async def auth(self):
        """
        Авторизовывает и запускаем клиент
        """

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
                try:
                    await self.client.sign_in(password=input('Введите пароль: '))
                except:
                    logger.error('Ошибка авторизации.')
                    return False

        return True

