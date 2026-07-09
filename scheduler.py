import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot import bot, app
from config import TELEGRAM_CHAT_ID
from utils import format_for_telegram

def run_morning_brief():
    return app.invoke({"trigger_type": "morning_brief"})

async def async_morning_brief_job():
    print("⏰ Chạy Morning Brief Job...")
    try:
        final_state = await asyncio.to_thread(run_morning_brief)
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=format_for_telegram(final_state["final_response"]))
    except Exception as e:
        print(f"Lỗi khi gửi Morning Brief: {e}")

def setup_scheduler():
    scheduler = AsyncIOScheduler()
    # Chạy mỗi ngày lúc 8:00 AM giờ Việt Nam
    scheduler.add_job(
        async_morning_brief_job, 
        'cron', 
        hour=8, 
        minute=0, 
        timezone='Asia/Ho_Chi_Minh', 
        id="morning_brief"
    )
    scheduler.start()
    print("📅 Scheduler started!")
