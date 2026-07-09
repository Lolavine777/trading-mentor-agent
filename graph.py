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
from mentor import get_model, build_market_data_context, build_macro_context, build_portfolio_context, build_memory_context
from config import temperature
from macro import fetch_macro_data

# --- 2. Khai báo các Node (Các hàm xử lý cục bộ) ---
def supervisor_node(state: AgentState):
    return {"messages": [AIMessage(content="Supervisor đã tiếp nhận yêu cầu.")]}

def market_node(state: AgentState):
    try:
        # Lấy 2 mã đầu tiên trong Portfolio để test cho nhanh
        symbols = [p["symbol"] for p in PORTFOLIO][:2]
        analyses = analyze_portfolio(symbols)
        return {"market_data": {"analyses": analyses}}
    except Exception as e:
        return {"market_data": {"error": f"Lỗi Vnstock: {str(e)}", "analyses": []}}

def macro_node(state: AgentState):
    macro_data = fetch_macro_data()
    return {"macro_data": macro_data}

def portfolio_node(state: AgentState):
    # Trả về danh mục hiện tại (có thể sau này đọc từ file)
    return {"portfolio_data": {"holdings": PORTFOLIO}}

def analyst_node(state: AgentState):
    market_raw = state.get("market_data", {})
    analyses = market_raw.get("analyses", [])
    market_error = market_raw.get("error")

    macro_raw = state.get("macro_data", {})
    portfolio_raw = state.get("portfolio_data", {}).get("holdings", [])

    memory = build_memory_context()
    
    if market_error:
        market_context = f"## MARKET DATA\nLỗi: Không thể lấy dữ liệu thị trường hôm nay ({market_error}). Hãy báo cáo lỗi này và chỉ phân tích dựa trên Vĩ mô và Danh mục."
    else:
        market_context = build_market_data_context(analyses)
        
    macro_context = build_macro_context(macro_raw)
    portfolio_context = build_portfolio_context(portfolio_raw)
    
    prompt = f"{memory}\n\n{macro_context}\n\n{portfolio_context}\n\n{market_context}\n\nHãy phân tích dữ liệu trên để viết bản tin."
    model = get_model()
    
    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": temperature}
    )
    return {"analyst_output": response.text}

def formatter_node(state: AgentState):
    raw_text = state.get("analyst_output", "")
    final_text = f"🌞 **BẢN TIN SÁNG** 🌞\n\n{raw_text}\n\n_Chúc sếp một ngày giao dịch hiệu quả!_"
    return {"final_response": final_text}

def tutor_node(state: AgentState):
    user_intent = state.get("user_intent", "")
    memory = build_memory_context()
    
    prompt = f"{memory}\n\nNgười dùng hỏi: {user_intent}\n\nHãy phân tích và trả lời như một người thầy dạy về đầu tư chứng khoán."
    model = get_model(prompt_name="tutor")
    
    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": temperature}
    )
    return {"final_response": response.text}

# --- 3. Hàm Router (Định tuyến) ---
# Trả về list các node để chạy song song (LangGraph Fan-out)
def route_supervisor(state: AgentState) -> list[str]:
    if state.get("trigger_type") == "morning_brief":
        return ["market", "macro", "portfolio"]
    elif state.get("trigger_type") == "chat":
        return ["tutor"]
    return ["END"]

# --- 4. Lắp ráp đồ thị (Graph) ---
def build_graph():
    workflow = StateGraph(AgentState)
    
    # Đăng ký các Node
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("market", market_node)
    workflow.add_node("macro", macro_node)
    workflow.add_node("portfolio", portfolio_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("formatter", formatter_node)
    workflow.add_node("tutor", tutor_node)
    
    # Định nghĩa luồng chạy (Edges)
    workflow.add_edge(START, "supervisor")
    
    # Fan-out: rẽ nhánh song song
    workflow.add_conditional_edges(
        "supervisor",
        route_supervisor,
        ["market", "macro", "portfolio", "tutor", END]
    )
    
    # Fan-in: hội tụ về analyst
    workflow.add_edge("market", "analyst")
    workflow.add_edge("macro", "analyst")
    workflow.add_edge("portfolio", "analyst")
    
    workflow.add_edge("analyst", "formatter")
    workflow.add_edge("formatter", END)
    workflow.add_edge("tutor", END)
    
    # Biên dịch (Compile)
    app = workflow.compile()
    return app
