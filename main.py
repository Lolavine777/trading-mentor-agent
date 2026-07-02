import os
import sys
import io

# Fix lỗi in Emoji trên Windows (CP1252 -> UTF-8)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Đảm bảo import đúng đường dẫn
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph import build_graph

def main():
    print("🚀 Đang khởi tạo Trading Mentor Agent (LangGraph)...")
    app = build_graph()
    
    print("📡 Đang chạy kịch bản: Morning Brief...")
    # Khởi tạo State ban đầu
    initial_state = {
        "messages": [],
        "trigger_type": "morning_brief",
        "user_intent": "",
        "market_data": {},
        "macro_data": {},
        "portfolio_data": {},
        "analyst_output": "",
        "final_response": ""
    }
    
    # Chạy đồ thị
    final_state = app.invoke(initial_state)
    
    print("\n" + "="*50)
    print("📝 KẾT QUẢ TỪ FORMATTER NODE:")
    print("="*50 + "\n")
    print(final_state["final_response"])
    print("\n" + "="*50)

if __name__ == "__main__":
    main()
