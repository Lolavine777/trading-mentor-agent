import google.generativeai as genai
from pathlib import Path
from config import GEMINI_API_KEY, model_name, temperature
from analyst import analyze_portfolio
from memory_manager import build_memory_context
from portfolio import PORTFOLIO

genai.configure(api_key=GEMINI_API_KEY)

PROMPTS_DIR = Path(__file__).parent / "prompts"

def load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.txt").read_text(encoding="utf-8")

def get_model(prompt_name: str = "morning_brief"):
    instruction = load_prompt(prompt_name) if prompt_name else None
    return genai.GenerativeModel(
        model_name=model_name,
        system_instruction=instruction
    )

def build_market_data_context(analyses: list) -> str:
    lines = ["## MARKET DATA\n"]
    for a in analyses:
        if "error" in a:
            lines.append(f"- {a['symbol']}: Lỗi kéo data - {a['error']}")
            continue
        lines.append(
            f"- {a['symbol']}: close {a['close']:,}, "
            f"thay đổi {a['change_pct']}%, "
            f"volume {a['volume_note']}, "
            f"{a['interpretation']}"
        )
    return "\n".join(lines)

def build_macro_context(macro_data: dict) -> str:
    if not macro_data:
        return "## MACRO DATA\n(Chưa có dữ liệu vĩ mô)"
    if macro_data.get("error"):
        return f"## MACRO DATA\n(Lỗi lấy dữ liệu vĩ mô: {macro_data['error']})"
        
    lines = ["## MACRO DATA\n"]
    if macro_data.get("usd_vnd"):
        lines.append(f"- Tỷ giá USD/VND: {macro_data['usd_vnd']:,}")
    if macro_data.get("dow_jones"):
        dj = macro_data['dow_jones']
        lines.append(f"- Dow Jones: {dj['price']:,} (Thay đổi: {dj['change_pct']}%)")
    return "\n".join(lines)

def build_portfolio_context(holdings: list) -> str:
    if not holdings:
        return "## PORTFOLIO\n(Danh mục trống hoặc không lấy được dữ liệu)"
        
    lines = ["## PORTFOLIO\n"]
    for item in holdings:
        lines.append(f"- {item['symbol']}: {item['quantity']} cổ phiếu, giá vốn {item['buy_price']}")
    return "\n".join(lines)

def generate_morning_brief() -> str:
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=load_prompt("morning_brief")
    )
    symbols = [p["symbol"] for p in PORTFOLIO]
    analyses = analyze_portfolio(symbols)
    memory = build_memory_context()
    market_data = build_market_data_context(analyses)

    prompt = f"{memory}\n\n{market_data}\n\nHãy viết báo cáo buổi sáng."

    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": temperature}
    )
    return response.text

def generate_evening_review() -> str:
    model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=load_prompt("evening_review")
    )
    symbols = [p["symbol"] for p in PORTFOLIO]
    analyses = analyze_portfolio(symbols)
    memory = build_memory_context()
    market_data = build_market_data_context(analyses)

    prompt = f"{memory}\n\n{market_data}\n\nHãy viết báo cáo buổi tối."

    response = model.generate_content(
        contents=prompt,
        generation_config={"temperature": temperature}
    )
    return response.text