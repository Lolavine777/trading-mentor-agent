import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.client.default import DefaultBotProperties
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from graph import build_graph
from utils import format_for_telegram

# Khởi tạo bot và dispatcher
bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()
app = build_graph()

def check_chat_id(message: types.Message) -> bool:
    return str(message.chat.id) == str(TELEGRAM_CHAT_ID)

@dp.message(CommandStart())
async def handle_start_command(message: types.Message):
    if not check_chat_id(message):
        return
    await message.answer("Xin chào! Tôi là Trading Mentor Agent. Gõ /brief để nhận bản tin sáng, hoặc chat bất kỳ điều gì để trao đổi!")

@dp.message(Command("brief"))
async def handle_brief_command(message: types.Message):
    if not check_chat_id(message):
        return
    await message.answer("Đang tải dữ liệu thị trường, sếp đợi một lát nhé...")
    
    # Chạy LangGraph (đồng bộ) trên một thread khác để không block Telegram event loop
    final_state = await asyncio.to_thread(app.invoke, {"trigger_type": "morning_brief"})
    await message.answer(format_for_telegram(final_state["final_response"]))

@dp.message()
async def handle_chat_message(message: types.Message):
    if not check_chat_id(message):
        return
    
    # Chạy LangGraph (đồng bộ) trên một thread khác
    final_state = await asyncio.to_thread(
        app.invoke, 
        {"trigger_type": "chat", "user_intent": message.text}
    )
    await message.answer(format_for_telegram(final_state["final_response"]))

async def start_bot():
    print("🤖 Telegram Bot started!")
    await dp.start_polling(bot)
