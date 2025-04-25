import asyncio
import logging
import os

import aiohttp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
API_BASE_URL = "http://localhost:8000/api/v1"

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

choice_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📄 Отримати підсумок")],
        [KeyboardButton(text="📝 Отримати зміст та тези")]
    ],
    resize_keyboard=True
)

new_file_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📤 Завантажити новий файл")],
        [KeyboardButton(text="🔁 Повернутися до поточного файлу")]
    ],
    resize_keyboard=True
)

user_docs = {}


@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привіт! Надішли мені документ (.txt), і я підготую для тебе підсумок або зміст та тези.")


@dp.message(F.document)
async def handle_document(message: types.Message):
    file = message.document
    if not file.file_name.endswith(".txt"):
        await message.answer("Будь ласка, надішли текстовий файл (.txt)")
        return

    file_path = f"temp/{file.file_id}.txt"
    os.makedirs("temp", exist_ok=True)
    await bot.download(file, destination=file_path)

    user_docs[message.from_user.id] = file_path
    await message.answer("Документ отримано! Обери, що з ним зробити:", reply_markup=choice_keyboard)


@dp.message(F.text.in_(["📄 Отримати підсумок", "📝 Отримати зміст та тези"]))
async def handle_choice(message: types.Message):
    user_id = message.from_user.id
    file_path = user_docs.get(user_id)

    if not file_path or not os.path.exists(file_path):
        await message.answer("Файл не знайдено. Надішли, будь ласка, файл ще раз.")
        return

    endpoint = "/get_summary" if message.text == "📄 Отримати підсумок" else "/get_contents_and_theses"

    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            form = aiohttp.FormData()
            form.add_field("file", f, filename="document.txt", content_type="text/plain")

            async with session.post(API_BASE_URL + endpoint, data=form) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    key = "summary" if "summary" in data else "contents"
                    await message.answer(data[key])
                else:
                    await message.answer("Виникла помилка при обробці файлу.")

    await message.answer("Що хочеш робити далі?", reply_markup=new_file_keyboard)


# Оновлені методи для роботи з новим файлом або поточним
@dp.message(F.text == "📤 Завантажити новий файл")
async def handle_new_file(message: types.Message):
    await message.answer("Будь ласка, надішли новий файл для обробки.")
    user_docs.pop(message.from_user.id, None)


@dp.message(F.text == "🔁 Повернутися до поточного файлу")
async def handle_current_file(message: types.Message):
    user_id = message.from_user.id
    file_path = user_docs.get(user_id)

    if not file_path or not os.path.exists(file_path):
        await message.answer("Файл не знайдено. Надішли, будь ласка, файл ще раз.")
        return

    await message.answer("Вибери, що з поточним файлом зробити:", reply_markup=choice_keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
