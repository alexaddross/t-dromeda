from markups import main_menu
from telebot import TeleBot
from requests import get
from utils.common import load_robot_data
from utils.message_formatters import bags_formatter
import json

bot = TeleBot('6343881202:AAEBAXFJMKTcIunpBkXfzoAIZiT8vp2F0Z0')


@bot.message_handler()
def main_handler(message):
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id, 'Здравствуйте! Я -- система удалённого мониторинга кампании Transconvey. Для авторизации, пожалуйста, отправьте серийный номер Вашего робота (его можно найти на шильдах на роботе).', reply_markup=main_menu)
    elif message.text.lower() == 'мешки':
        response = get('http://127.0.0.1:8000/get_robot_data/')
        robot_data = load_robot_data(response)

        bot.send_message(message.from_user.id, bags_formatter(robot_data), parse_mode='HTML')


bot.polling(non_stop=True)