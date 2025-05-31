from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN = "8175491637:AAF_-6-4EeUN-hkvhcdhmdQ9RdpmDGrts8s"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://flask-1-kjvz.onrender.com{WEBHOOK_PATH}"

# Исправленная инициализация бота
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):
    await message.answer("Привет, я бот")

@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
