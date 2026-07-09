
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

## 2026-07-02 -> 2026-07-07 session 4
- Xong: Khởi tạo Project Kickoff, thiết lập `AGENTS.md` (TDD, Hard Rules).
- Xong: Xây dựng core LangGraph trong `graph.py` (State Reducer, Supervisor Routing, Data Nodes).
- Xong: Áp dụng TDD viết `tests/test_graph.py` chạy Pass luồng E2E Graph.
- Xong: Tạo `main.py`, kết nối Vnstock và Gemini (`gemini-3.5-flash`), xuất báo cáo ra Terminal. Đã fix lỗi Unicode Windows.

- Xong: Triển khai Phase 2: Multi-Agent & Data Sources (Fan-out / Fan-in parallel execution trong LangGraph).
- Xong: Thêm `macro.py` (yfinance), `portfolio_node`, và xử lý Graceful Degradation ở `market_node`.
- Xong: Update prompt LLM để gộp Vĩ mô, Danh mục và Thị trường vào chung bản tin sáng.
- Tiếp theo (Phase 3): Tích hợp API Telegram (aiogram) và Cron scheduler (APScheduler) để biến thành Bot tương tác thực thụ.

## 2026-07-09 session 5
- Xong: Tích hợp thư viện `aiogram` để tạo Telegram Bot và `APScheduler` để hẹn giờ.
- Xong: Áp dụng TDD (viết fail tests trước khi code) cho `bot.py` và `scheduler.py`.
- Xong: Update `graph.py` thêm `tutor_node` nhận diện chat tự do và giải thích kiến thức đầu tư dựa trên Memory.
- Tiếp theo (Phase 4): Nâng cấp `supervisor_node` từ Rule-based tĩnh thành Semantic Router (dùng LLM) để tự phân tích intent và điều hướng tới các node phù hợp thay vì code cứng `if/else`.
- Xong (Bug Fix): Đã xử lý lỗi compile Markdown trên Telegram bằng cách thêm `utils.py` để chuyển định dạng sang Telegram HTML (hỗ trợ `<b>`, `<i>`, `<code>`, `<a>`) và cấu hình `parse_mode="HTML"` cho Bot.