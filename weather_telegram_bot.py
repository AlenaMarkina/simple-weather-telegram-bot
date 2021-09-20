# python3
# weather_telegram_bot.py - simple telegram bot which returns current temperature of the entered city


import os
from os.path import join, dirname
import requests
from flask import Flask
from flask import request
from dotenv import load_dotenv

app = Flask(__name__)


# Возвращает из файла .env значение по ключу
def get_from_env(key):
    path = join(dirname(__file__), '.env')
    load_dotenv(path)
    return os.environ.get(key)


# Принимает в качестве аргумента название города и возвращает текущюю температуру в этом городе.
def get_weather(city):
    api_key = get_from_env('OPENWEATHERMAP_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        temperature = weather_data['main']['temp']
        return temperature


# Отправляет сообщение в телеграм бота
def send_message(chat_id, text):
    method = "sendMessage"  # метод телеграмма для отправки текстовых сообщений
    token = get_from_env('TELEGRAM_BOT_TOKEN')  # получаем секретный токен телеграмма
    url = f"https://api.telegram.org/bot{token}/{method}"
    data_to_send = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data_to_send)


@app.route("/", methods=['POST'])
def process():
    chat_id = request.json['message']['chat']['id']  # получаем id чата из данных в формате json, которые приходят от телеграмм
    city_name = request.json['message']['text']  # получаем название города
    current_temperature = get_weather(city_name)  # получаем текущюю температуру
    send_text = f'Текущая температура воздуха {current_temperature}°C'
    send_message(chat_id=chat_id, text=send_text)
    return {"ok": True}


if __name__ == '__main__':
    app.run(debug=True)
