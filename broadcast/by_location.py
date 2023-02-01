import requests
import datetime
import config.tokens as tokens
import config.params as params


weather_emodji = params.weather_emodji


def broadcastByLocation(location):
	if location is not None:
		lat = location["latitude"]
		lon = location["longitude"]
		response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid={tokens.WEATHER_TOKEN}")
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

		
		return text
	else:
		return "Ошибка в локации!"
