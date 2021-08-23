"""

Файл с текстами ответов

"""
import telebot

MESSAGES = {
    'keyboards': {
        'send_phone': 'Отправить номер телефона',
        'MAIN': {
            'buy_sub': 'Купить подписку',
            'search': 'Начать поиск',
        },
        'SEARCH': {
            'start_again': 'Новый поиск',
            'go_main': 'Вернуться в главное меню',
        }
    },

    '/start': 'Добро пожаловать в бота "Глаз Бога". Пройдите простую процедуру регистрации (входа), '
              'отправив нам свой номер телефона:',

    'successful_registration': 'Успешная регистрация.',

    'MAIN_STATE': 'Вы зарегистрировались: {reg_dt}\nВас счёт: {money_count}\nПодписка действительна до: {subs_due}',
    'SEARCH_STATE': 'Введите данные для поиска:',
    'end_search': 'Поиск завершён. Выберите дальнейшие действия с помощью кнопок внизу.',


    'no_command': 'Нет такой команды. Выберите кнопку снизу.'

}


class KEYBOARDS(object):

    def phone_keyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button_phone = telebot.types.KeyboardButton(text=MESSAGES['keyboards']['send_phone'], request_contact=True)
        keyboard.add(button_phone)
        return keyboard

    def main_keyboard(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button = telebot.types.KeyboardButton(text=MESSAGES['keyboards']['MAIN']['buy_sub'])
        keyboard.add(button)

        button = telebot.types.KeyboardButton(text=MESSAGES['keyboards']['MAIN']['search'])
        keyboard.add(button)

        return keyboard

    def end_search(self):
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        button = telebot.types.KeyboardButton(text=MESSAGES['keyboards']['SEARCH']['start_again'])
        keyboard.add(button)

        button = telebot.types.KeyboardButton(text=MESSAGES['keyboards']['SEARCH']['go_main'])
        keyboard.add(button)

        return keyboard


Keyboards = KEYBOARDS()
