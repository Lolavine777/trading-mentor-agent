import os
import sys
import io
import asyncio

# Fix lỗi in Emoji trên Windows (CP1252 -> UTF-8)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đảm bảo import đúng đường dẫn
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot import start_bot
from scheduler import setup_scheduler

async def main():
    print("🚀 Đang khởi tạo Trading Mentor Agent (Aiogram + LangGraph)...")
    setup_scheduler()
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
