import operator
from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, START, END

# --- 1. Định nghĩa State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    trigger_type: str
    user_intent: str
    market_data: dict
    macro_data: dict
    portfolio_data: dict
    analyst_output: str
    final_response: str

from analyst import analyze_portfolio
from portfolio import PORTFOLIO
from mentor import get_model, build_market_data_context, build_memory_context
from config import temperature

# --- 2. Khai báo các Node (Các hàm xử lý cục bộ) ---
def supervisor_node(state: AgentState):
    return {"messages": [AIMessage(content="Supervisor đã tiếp nhận yêu cầu.")]}

def market_node(state: AgentState):
    # Lấy 2 mã đầu tiên trong Portfolio để test cho nhanh
    symbols = [p["symbol"] for p in PORTFOLIO][:2]
    analyses = analyze_portfolio(symbols)
    return {"market_data": {"analyses": analyses}}

def analyst_node(state: AgentState):
    analyses = state.get("market_data", {}).get("analyses", [])
    memory = build_memory_context()
    market_context = build_market_data_context(analyses)
    
    prompt = f"{memory}\n\n{market_context}\n\nHãy phân tích dữ liệu trên."
    model = get_model()
    
    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": temperature}
    )
    return {"analyst_output": response.text}

def formatter_node(state: AgentState):
    raw_text = state.get("analyst_output", "")
    # Tạm thời format bằng Python cơ bản
    final_text = f"🌞 **BẢN TIN SÁNG** 🌞\n\n{raw_text}\n\n_Chúc sếp một ngày giao dịch hiệu quả!_"
    return {"final_response": final_text}

# --- 3. Hàm Router (Định tuyến) ---
def route_supervisor(state: AgentState) -> Literal["market", "END"]:
    if state.get("trigger_type") == "morning_brief":
        return "market"
    return "END"

# --- 4. Lắp ráp đồ thị (Graph) ---
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Đăng ký các Node
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("market", market_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("formatter", formatter_node)
    
    # Định nghĩa luồng chạy (Edges)
    workflow.add_edge(START, "supervisor")
    
    # Rẽ nhánh từ Supervisor
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "market": "market",
            "END": END
        }
    )
    
    # Nối theo chiều dọc (Tuyến tính)
    workflow.add_edge("market", "analyst")
    workflow.add_edge("analyst", "formatter")
    workflow.add_edge("formatter", END)
    
    # Biên dịch (Compile)
    app = workflow.compile()
    return app
