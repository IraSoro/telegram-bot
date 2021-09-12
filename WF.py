
import telebot
import requests
from telebot import types
from glob import glob
from random import choice

bot = telebot.TeleBot("token")
access_token = ""


@bot.message_handler(content_types=['text', 'document', 'audio'])
def start(message):
    if message.text == "/hello":
        bot.send_message(message.from_user.id,
                         "Привет! Если хочешь узнать прогноз погоды,"
                         "введи /wf")
    elif message.text == "/wf":
        city(message)
    else:
        bot.send_message(message.from_user.id,
                         "Чтобы начать работать, введи /hello")


def city(message):
    if message.text == "/wf":
        keyboard = types.InlineKeyboardMarkup()
        key_st = types.InlineKeyboardButton(
            text="Санкт-Петербург", callback_data="st")
        keyboard.add(key_st)
        key_nn = types.InlineKeyboardButton(
            text="Нижний Новгород", callback_data="nn")
        keyboard.add(key_nn)
        question = "Чтобы показать тебе прогноз погоды, мне нужно узнать твой"\
                   " город. Выбери нужный:"
        bot.send_message(message.from_user.id, text=question,
                         reply_markup=keyboard)

        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            if call.data == "st":
                s_city = "Russia, St.Peterburg"
            elif call.data == "nn":
                s_city = "Russia, Nizhny Novgorod"
            get_param(message, s_city)

    else:
        bot.send_message(message.from_user.id, 'Напиши /wf')


def get_param(message, s_city):
    city_id = 0
    appid = "буквенно-цифровой APPID"
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                           params={'q': s_city,
                                   'units': 'metric',
                                   'lang': 'ru',
                                   'APPID': f'{access_token}'
                                   }
                           )
        data = res.json()
        temp = data['list'][0]['main']['temp']
        description = data['list'][0]['weather'][0]['description']
        clouds = data['list'][0]['clouds']['all']
        rain = data['list'][0]['rain']
        snow = data['list'][0]['snow']
        get_weather(message, temp, description, clouds, rain, snow)
    except Exception as e:
        print("Exception (weather):", e)
        pass


def get_weather(message, temp, description, clouds, rain, snow):
    wf = f"Сегодня ожидается {temp} градусов по Цельсию\n" \
         f"В целом, будет {description}\n" \
         f"Облачно на {clouds}%\n"
    if str(rain) == "None":
        wf += "Дождь не предвидится\n"
    else:
        wf += f"Дождь: {rain}%\n"
    if str(snow) == "None":
        wf += "Снег не планируется"
    else:
        wf += f"Снег: {snow}%"
    bot.send_message(message.from_user.id, wf)
    get_random_alpacas(message)
    sun = "И пусть в любую погоду у тебя всегда будет солнышко в душе" \
          " и солнышко на небе☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️☀️"
    bot.send_message(message.from_user.id,  sun)


def get_random_alpacas(message):
    try:
        list = glob("alpacas/*")
        picture = choice(list)
        bot.send_photo(chat_id=message.chat.id, photo=open(picture, "rb"))
    except Exception as e:
        print("Exception (picture):", e)
        pass


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
