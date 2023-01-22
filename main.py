# перенести токенЫ в другой файл
# указывать скорость ветра и учесть зависимость скорости ветра от того, как ощущается температура на самом деле
# прогноз за 3 дня
# определение погоды по координатам
# Кнопки из наболее частых запросов
# Удаление такой кнопки или ее создание
# Загрязняемость воздуха
# Напоминание утром какая погода и какая погода ожидается через 3-4 час
# Записываем id пользователя в файл и там же указываем какой город он выбрал. Если пользователь выбирает другой город, то мы его перезаписываем
import telebot
from telebot import types
#from pyowm import OWM

from pyowm.utils import timestamps
from pyowm.owm import OWM

from pyowm.utils.config import get_default_config
bot = telebot.TeleBot("5731675039:AAGfp9qenNkX0qJ2ycLaMein8khUt9PhJWM", parse_mode=None)

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('f93aeb547d35a1f94090715eab9634f2', config_dict)

@bot.message_handler(commands=['start'])
def send_welcome(message):

	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton(text="Выбрать город", callback_data='get_town')
	btn2 = types.InlineKeyboardButton(text='Погода на конкретную дату', callback_data='get_needed_date')

	markup.add(btn1, btn2)
	bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я тестовый бот. В данный момент я могу показать тебе прогноз погоды в конкретном городе.".format(message.from_user), reply_markup=markup)

@bot.callback_query_handler(func = lambda call:True)
def answer(call):
	if call.data =='get_town':
		mesg = bot.send_message(call.from_user.id, 'Погода в каком городе тебя интересует?')
	elif call.data =='get_needed_date':
		bot.send_message(call.from_user.id, text="Раздел в разработке")
	elif call.data =='get_tomorrow_weather':
		bot.send_message(call.from_user.id, text="Раздел в разработке")
	elif call.data == 'three_days_weather':
		bot.send_message(call.from_user.id, text="Раздел в разработке")


@bot.message_handler(content_types=['text'])
# def get_town(message):
# 	bot.reply_to(message, "О, я был там. Прекрасное место!")
# 	town = message.text
# 	bot.register_next_step_handler(message, message_reply(town))


def message_reply(message):

			bot.send_message(message.chat.id, text="Ищу информацию о погоде искомом городе")
			mgr = owm.weather_manager()
			observation = mgr.weather_at_place(message.text)
			w = observation.weather
			temperature = w.temperature('celsius')["temp"]
			answer = 'В городе ' + message.text + ' сейчас ' + w.detailed_status + '\n'
			answer += 'Температура сейчас в районе ' + str(temperature) + '°С'+'\n'

			markup = types.InlineKeyboardMarkup()
			button_tomorrow = types.InlineKeyboardButton(text="Погода на завтра", callback_data='get_tomorrow_weather')
			button_3_days = types.InlineKeyboardButton(text='Прогноз на 3 дня', callback_data='three_days_weather')
			button_choose_place = types.InlineKeyboardButton(text='Выбрать город', callback_data='get_town')

			markup.add(button_tomorrow, button_3_days, button_choose_place)
		#bot.send_message(message.char.id, str(place))
			bot.send_message(message.chat.id, answer, reply_markup = markup)

		# if message == "Ищу погоду в выбранном городе на завтра":
		# 	mgr = owm.weather_manager()
		# 	daily_forecaster = mgr.forecast_at_place(place, 'daily')
		# 	tomorrow = timestamps.tomorrow()  # datetime object for tomorrow
		# 	weather = daily_forecaster.get_weather_at(tomorrow)


bot.infinity_polling()