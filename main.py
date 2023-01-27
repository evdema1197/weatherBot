from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import BOT_TOKEN
from broadcast import broadcastByLocation, broadcastByName
from keyboards import start_kb


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
	

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название своего города!", reply_markup=start_kb())


@dp.message_handler()
async def broadcast_send(message: types.Message):
	await message.answer(text=broadcastByName(message.text))


@dp.message_handler(content_types=['location'])
async def location (message):
	await message.answer(text=broadcastByLocation(message.location))


if __name__ == "__main__":
	executor.start_polling(dispatcher=dp, skip_updates=True)
