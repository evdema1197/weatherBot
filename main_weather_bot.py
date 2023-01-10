from aiogram import Bot, Dispatcher,executor, types
from config import TOKEN_API, WEATHER_TOKEN
from pprint import pprint
import datetime
import requests

bot= Bot(token=TOKEN_API)
dp= Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название своего города!")

@dp.message_handler()
async def get_weather(message: types.Message):
    weather_emodji={
		"Clear": "Ясно \U00002600",
		"Clouds": "Облачно \U00002601",
		"Rain": "Дождь \U00002614",
		"Drizzle": "Дождь \U00002614",
		"Thunderstorm": "Гроза \U000026A1",
		"Snow": "Снег \U0001F328"
		}
    try:
        r_lat_lon = requests.get(
			f'http://api.openweathermap.org/geo/1.0/direct?q={message.text}&limit=1&appid={WEATHER_TOKEN}'
			)
        data = r_lat_lon.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        r = requests.get(
			f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={WEATHER_TOKEN}"
		)
        weather_data=r.json()

        name=weather_data["name"]
        feels_like=weather_data["main"]["feels_like"]
        temp=weather_data["main"]["temp"]
        pressure=weather_data["main"]["pressure"]
        humidity=weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]
        sunrise=datetime.datetime.fromtimestamp((weather_data["sys"]["sunrise"]))

        weather_descrition=weather_data["weather"][0]["main"]
        if  weather_descrition in weather_emodji:
            wd = weather_emodji[weather_descrition]
        else:
            wd=" "

        await message.reply(f"Погода в городе: {name} {wd}\nТемпература: {temp} °C\n"
		f"Ощущается как: {feels_like} °С\nВлажность: {humidity} %\n"
		f"Давление: {pressure} \nСкорость ветра: {wind_speed} м/c\n"
		f"Восход солнца: {sunrise}\n"
		f"Хорошего дня 🧡"
		)
    except Exception as ex:
        await message.reply(ex)
        await message.reply("Проверьте название города")

if __name__== '__main__':
    executor.start_polling(dp,skip_updates=True)