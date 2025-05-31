import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Update
from aiogram.fsm.storage.memory import MemoryStorage

BOT_TOKEN = "8175491637:AAF_-6-4EeUN-hkvhcdhmdQ9RdpmDGrts8s"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://flask-1-kjvz.onrender.com{WEBHOOK_PATH}"

bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# Храним активных пользователей
users = set()

@dp.message(commands=["start"])
async def start_cmd(message: types.Message):
    users.add(message.chat.id)
    await message.answer("Привет, я бот")

# Обработка вебхука
@app.post(WEBHOOK_PATH)
async def webhook_handler(request: Request):
    data = await request.json()
    update = Update.model_validate(data)
    await dp.feed_update(bot, update)
    return {"ok": True}

# Установка вебхука и запуск фоновой задачи
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(live_notifier())

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()

# Периодическая задача
async def live_notifier():
    while True:
        for user_id in users:
            try:
                await bot.send_message(user_id, "Я жив")
            except:
                pass
        await asyncio.sleep(300)
