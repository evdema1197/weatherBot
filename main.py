from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN_API, WEATHER_TOKEN
from pprint import pprint
import datetime
import requests


weather_emodji = {
		"Clear": "Ясно \U00002600",
		"Clouds": "Облачно \U00002601",
		"Rain": "Дождь \U00002614",
		"Drizzle": "Дождь \U00002614",
		"Thunderstorm": "Гроза \U000026A1",
		"Snow": "Снег \U0001F328"
		}


bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)


def get_keyboard() -> ReplyKeyboardMarkup:
	return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Погода по локации", request_location=True))
	

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название своего города!", reply_markup=get_keyboard())


def get_broadcast_name(city):
	try:
		params = {"q": f"{city}", "appid": WEATHER_TOKEN, "units": "metric", "lang": "ru"}
		response = requests.get("https://api.openweathermap.org/data/2.5/weather", params=params)
		w_request = response.json()
		name=w_request["name"]
		feels_like=w_request["main"]["feels_like"]
		temp=w_request["main"]["temp"]
		pressure=w_request["main"]["pressure"]
		humidity=w_request["main"]["humidity"]
		wind_speed = w_request["wind"]["speed"]
		sunrise=datetime.datetime.fromtimestamp((w_request["sys"]["sunrise"]))

		weather_descrition=w_request["weather"][0]["main"]
		if  weather_descrition in weather_emodji:
			wd = weather_emodji[weather_descrition]
		else:
			wd=" "
		
		message = (f"Погода в городе: {name} {wd}\nТемпература: {temp} °C\n"
		f"Ощущается как: {feels_like} °С\nВлажность: {humidity} %\n"
		f"Давление: {pressure} \nСкорость ветра: {wind_speed} м/c\n"
		f"Восход солнца: {sunrise}\n"
		f"Хорошего дня 🧡")

		return message

	except Exception:
		return "Проверьте название города!"


@dp.message_handler()
async def broadcast_send(message: types.Message):
	await message.answer(text=get_broadcast_name(message.text))


@dp.message_handler(content_types=['location'])
async def location (message):
	if message.location is not None:
		print(message.location)
		lat = message.location["latitude"]
		lon = message.location["longitude"]
		response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={WEATHER_TOKEN}")
		w_request = response.json()
		name=w_request["name"]
		feels_like=w_request["main"]["feels_like"]
		temp=w_request["main"]["temp"]
		pressure=w_request["main"]["pressure"]
		humidity=w_request["main"]["humidity"]
		wind_speed = w_request["wind"]["speed"]
		sunrise=datetime.datetime.fromtimestamp((w_request["sys"]["sunrise"]))

		weather_descrition=w_request["weather"][0]["main"]
		if  weather_descrition in weather_emodji:
			wd = weather_emodji[weather_descrition]
		else:
			wd=" "
		
		text = (f"Погода в городе: {name} {wd}\nТемпература: {temp} °C\n"
		f"Ощущается как: {feels_like} °С\nВлажность: {humidity} %\n"
		f"Давление: {pressure} \nСкорость ветра: {wind_speed} м/c\n"
		f"Восход солнца: {sunrise}\n"
		f"Хорошего дня 🧡")
		await message.answer(text)


if __name__ == "__main__":
	executor.start_polling(dispatcher=dp, skip_updates=True)
