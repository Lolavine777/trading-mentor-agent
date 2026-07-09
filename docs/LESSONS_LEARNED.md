# Bài Học Kinh Nghiệm (Lessons Learned)

Tài liệu này ghi lại các bài học, nguyên tắc kiến trúc và những hiểu lầm đã được đính chính trong quá trình phát triển Trading Mentor Agent.

### 2026-07-07 - Xử lý ngoại lệ trong hệ thống Agentic (Graceful Degradation)
- **Bối cảnh:** Lấy dữ liệu thị trường (Vnstock) cho bản tin sáng.
- **Hiểu lầm/Sai lầm:** Chỉ bọc lệnh gọi API trong khối `try-except` và trả về biến rỗng khi gặp lỗi.
- **Cách tiếp cận đúng:** Trong kiến trúc LangGraph, State đóng vai trò là Contract giữa các Node. Node bắt lỗi phải trả về State một Payload hợp lệ chứa cờ báo lỗi (Error Flag), ví dụ: `{"market_data": {"error": "Lỗi kết nối", "analyses": []}}`. Sau đó, Node tiêu thụ (như LLM Prompt Builder) sẽ đọc cờ này để sinh ra Prompt dự phòng (fallback).
- **Tại sao quan trọng:** Tránh sụp đổ dây chuyền (Downstream Crash) do `KeyError` và tránh hiện tượng Ảo giác (Hallucination) của LLM khi bị mớm dữ liệu rỗng mà không được giải thích rõ. Đảm bảo hệ thống tự chữa lành (Self-healing).

### 2026-07-07 - Kiến trúc Chạy song song trong LangGraph (Fan-out / Fan-in)
- **Bối cảnh:** Lấy dữ liệu đồng thời từ nhiều nguồn (Vnstock, yfinance, local json) để giảm thời gian chờ của toàn bộ hệ thống.
- **The Mistake/Misconception:** Nghĩ rằng phải dùng các primitive phức tạp (như `Send` API của LangGraph) hoặc tự viết multithreading (ví dụ dùng `concurrent.futures`) để chạy nhiều node cùng lúc.
- **The Correct Approach:** Tận dụng cơ chế định tuyến (Conditional Edge) mặc định của LangGraph. Ở node phân bổ (`supervisor`), chỉ cần trả về một danh sách các node tiếp theo (VD: `return ["market", "macro", "portfolio"]`). LangGraph sẽ tự động ném các node này vào các thread chạy song song (Fan-out). Ở đầu ra, chỉ cần nối tất cả cạnh của 3 node này về chung node đích `analyst_node` (Fan-in). LangGraph sẽ tự động chờ cả 3 node chạy xong rồi mới kích hoạt `analyst_node`.
- **Tại sao quan trọng:** Giữ code cực kỳ tối giản (Pythonic), không sinh ra complexity không đáng có (như race condition) nhờ vào cơ chế quản lý State tự nhiên của LangGraph. Đảm bảo tốc độ ra bản tin nhanh nhất có thể.

### 2026-07-09 - Kiến trúc Semantic Router vs Rule-based cho LangGraph
- **Context:** Thiết kế luồng xử lý chat tự do trên Telegram Bot để phản hồi linh hoạt.
- **The Mistake/Misconception:** Nghĩ rằng có thể dùng lệnh `if/else` tĩnh (Rule-based) ở Supervisor node để điều hướng intent phức tạp.
- **The Correct Approach:** Thực chất cần một Semantic Router (gọi LLM làm Supervisor) để đọc input và tự quyết định kích hoạt Agent nào (Tool-calling Agent). Tuy nhiên, giải pháp thực dụng (Pragmatic) cho Phase 3 là route thẳng vào `tutor_node` đọc Memory, dời Semantic Router sang Phase 4 để tránh Over-engineering.
- **Why it matters:** Đảm bảo tiến độ ra mắt Bot an toàn thay vì đập đi xây lại cấu trúc lõi ngay lập tức.

### 2026-07-09 - LangGraph State Initialization (Partial Updates)
- **Context:** Khởi tạo `initial_state` để truyền vào `app.invoke()` tại các file bên ngoài (như `bot.py`, `scheduler.py`).
- **The Mistake/Misconception:** Nghĩ rằng phải khởi tạo cứng toàn bộ các key trong `AgentState` (kể cả giá trị rỗng như `market_data: {}`) mỗi khi gọi Graph, dẫn đến lặp code (redundant) và vi phạm DRY. Nhiều người nghĩ cần tạo một Class helper hoặc Factory method để khởi tạo.
- **The Correct Approach:** Trong LangGraph, `app.invoke()` hoạt động theo cơ chế **Partial State Update**. Ta CHỈ cần truyền vào những giá trị đầu vào (inputs) thực sự cần thiết (VD: `{"trigger_type": "chat", "user_intent": message.text}`). LangGraph sẽ tự động cập nhật State. Các node bên trong chỉ cần dùng `state.get("key", default)` là đủ an toàn.
- **Why it matters:** Giúp code cực kỳ Clean, đúng chuẩn DRY (Don't Repeat Yourself) và bám sát kiến trúc linh hoạt, tự nhiên của LangGraph.
