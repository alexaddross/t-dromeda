from telebot import TeleBot
from markups import main_menu

from requests import get, post

from utils.common import load_robot_data
from utils.message_formatters import bags_formatter
from utils.message_formatters import state_formatter

from config import *


bot = TeleBot('6343881202:AAEBAXFJMKTcIunpBkXfzoAIZiT8vp2F0Z0')


@bot.message_handler()
def main_handler(message):
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id, 'Здравствуйте! Я -- система удалённого мониторинга кампании Transconvey. Для авторизации, пожалуйста, отправьте серийный номер Вашего робота (его можно найти на шильдах на роботе).', reply_markup=main_menu)
        bot.register_next_step_handler(message, serial_got)
    elif message.text.lower() == 'мешки':
        response = get(f'http://{HOST}:{PORT}/get_robot_data/', json={'telegram_id': message.from_user.id})
        robot_data = load_robot_data(response)

        bot.send_message(message.from_user.id, bags_formatter(robot_data), parse_mode='HTML')
    elif message.text.lower() == 'состояние':
        response = get(f'http://{HOST}:{PORT}/get_robot_data/', json={'telegram_id': message.from_user.id})
        robot_data = load_robot_data(response)
        print(robot_data)
        bot.send_message(message.from_user.id, state_formatter(robot_data), parse_mode='HTML')


def serial_got(message):
    response = post(f'http://{HOST}:{PORT}/new_auth', json={'serial': message.text, 'telegram_id': message.from_user.id})

    if response.status_code != 202:
        bot.send_message(message.from_user.id, 'Извините, данный серийный номер в базе данных не зарегистрирован. Попробуйте ещё раз или обратитесь к производителю.')
        bot.register_next_step_handler(message, serial_got)
    else:
        bot.send_message(message.from_user.id, 'Добро пожаловать!\nВы успешно авторизованы, теперь вы можете пользоваться системой удалённого доступа Transconvey LLC.')
        bot.register_next_step_handler(message, main_handler)


bot.polling(non_stop=True)
