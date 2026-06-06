import json
from pathlib import Path
from datetime import datetime

MEMORY_DIR = Path(__file__).parent / "memory"

def _load(filename: str) -> dict:
    path = MEMORY_DIR / filename
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(filename: str, data: dict):
    path = MEMORY_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_portfolio() -> dict:
    return _load("portfolio.json")

def get_trade_history(days: int = 7) -> dict:
    data = _load("trade_history.json")
    if days:
        cutoff = datetime.today().strftime("%Y-%m-%d")
        recent = [
            t for t in data["trades"]
            if t["date"] >= cutoff[:8] + "01"  # đơn giản hóa
        ]
        data["trades"] = recent[-days:] if len(recent) > days else recent
    return data

def get_learning_progress() -> dict:
    return _load("learning_progress.json")

def build_memory_context() -> str:
    portfolio = get_portfolio()
    history = get_trade_history(days=7)
    learning = get_learning_progress()

    holdings_str = "\n".join([
        f"- {h['symbol']}: mua tại {h['buy_price']:,}, "
        f"số lượng {h['quantity']}, ngày {h['buy_date']}"
        for h in portfolio["holdings"]
    ]) or "Chưa có dữ liệu"

    mistakes_str = ", ".join([
        f"{k} x{v}" for k, v in history["mistake_patterns"].items() if v > 0
    ]) or "Chưa có"

    taught_str = ", ".join([
        c["concept"] for c in learning["concepts_taught"]
    ]) or "Chưa có"

    next_concept = (
        learning["concepts_queue"][0]
        if learning["concepts_queue"]
        else "Tự do chọn"
    )

    return f"""## MEMORY CONTEXT
Danh mục hiện tại:
{holdings_str}

Tiền mặt khả dụng: {portfolio['cash_available']:,} VND
Tổng đầu tư: {portfolio['total_invested']:,} VND

Lỗi hay gặp: {mistakes_str}
Số phiên đã học: {learning['sessions_completed']}
Khái niệm đã dạy: {taught_str}
Khái niệm tiếp theo nên dạy: {next_concept}
"""

def add_trade(trade: dict):
    data = _load("trade_history.json")
    trade["date"] = datetime.today().strftime("%Y-%m-%d")
    data["trades"].append(trade)
    if trade.get("mistake_type"):
        mistake = trade["mistake_type"]
        if mistake in data["mistake_patterns"]:
            data["mistake_patterns"][mistake] += 1
    _save("trade_history.json", data)

def mark_concept_taught(concept: str, context: str):
    data = _load("learning_progress.json")
    data["concepts_taught"].append({
        "concept": concept,
        "date_taught": datetime.today().strftime("%Y-%m-%d"),
        "context": context,
        "reinforced_count": 1
    })
    if concept in data["concepts_queue"]:
        data["concepts_queue"].remove(concept)
    data["sessions_completed"] += 1
    _save("learning_progress.json", data)

def update_portfolio(holdings: list, cash: int, total_invested: int):
    data = {
        "last_updated": datetime.today().strftime("%Y-%m-%d"),
        "holdings": holdings,
        "cash_available": cash,
        "total_invested": total_invested
    }
    _save("portfolio.json", data)