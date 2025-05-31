from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

BOT_TOKEN = "8175491637:AAF_-6-4EeUN-hkvhcdhmdQ9RdpmDGrts8s"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://flask-1-kjvz.onrender.com{WEBHOOK_PATH}"

# Инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Привет, я бот")

# FastAPI endpoint /ping
@app.get("/")
async def ping():
    return {"message": "I'm alive!"}

# Обработчик вебхука от Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# Установка вебхука при старте
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

# Удаление вебхука при остановке
@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
