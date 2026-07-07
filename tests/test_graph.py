import operator
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import pytest

# --- 1. Định nghĩa Contract cho State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    trigger_type: str
    user_intent: str
    market_data: dict
    macro_data: dict
    portfolio_data: dict
    analyst_output: str
    final_response: str

# Chúng ta import build_graph từ tệp graph.py (tệp này chúng ta chuẩn bị code)
from graph import build_graph

# --- 2. Bài Test E2E cho Phase 1 ---
def test_phase_1_graph_execution():
    """
    Kỳ vọng: Khi truyền trigger_type là 'morning_brief',
    đồ thị sẽ khởi chạy, đi qua các node (Market, Analyst...)
    và cuối cùng trả về final_response.
    """
    # 1. Dựng đồ thị
    app = build_graph()
    
    # 2. Bơm State ban đầu
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
    
    # 3. Chạy đồ thị
    final_state = app.invoke(initial_state)
    
    # 4. Kiểm thử kết quả
    assert "final_response" in final_state, "State bị thiếu trường final_response"
    assert len(final_state["final_response"]) > 0, "final_response không được rỗng"
    assert "analyst_output" in final_state, "State bị thiếu trường analyst_output"
    
    # Verify Phase 2 requirements (Parallel Nodes)
    assert "market_data" in final_state, "State bị thiếu trường market_data"
    assert "macro_data" in final_state, "State bị thiếu trường macro_data"
    assert "portfolio_data" in final_state, "State bị thiếu trường portfolio_data"
