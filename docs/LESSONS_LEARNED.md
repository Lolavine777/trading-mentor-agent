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
