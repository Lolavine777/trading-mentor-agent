
## 2026-06-07 session 2
- Xong: analyst.py với Vnstock 4.0 + pandas-ta, test với VIC/VHM/GEX data thật
- Tiếp theo: mentor.py, gọi Gemini API, inject memory + system prompt + market data
- Lưu ý: days=120 để đủ data cho EMA50

## 2026-06-08 session 3
- Xong: mentor.py load prompt từ file, generate_morning_brief chạy với data thật
- Bug 1: ngày hardcode 24/05, fix bằng inject datetime vào prompt
- Bug 2: model string "gemini-3-flash" không đúng, cần chạy list_models() để lấy string chính xác
- Tiếp theo: fix 2 bug trên, sau đó build main.py + scheduler.py + Telegram integration
- Note với agent: đã sửa lỗi 2, do sai tên model rồi;