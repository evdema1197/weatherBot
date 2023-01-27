from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_kb() -> ReplyKeyboardMarkup:
	return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text="Погода по локации", request_location=True))
