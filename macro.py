import yfinance as yf
import logging

def fetch_macro_data() -> dict:
    """
    Lấy dữ liệu vĩ mô (Tỷ giá USD/VND và Dow Jones) từ yfinance.
    Có xử lý Exception (Graceful Degradation) để không làm sập luồng LangGraph.
    """
    result = {
        "usd_vnd": None,
        "dow_jones": None,
        "error": None
    }
    
    try:
        # Lấy tỷ giá USD/VND
        usdvnd = yf.Ticker("USDVND=X")
        # fast_info là cách truy cập nhanh dữ liệu giá hiện tại trong yfinance mới
        usd_price = usdvnd.fast_info['last_price']
        
        # Lấy chỉ số Dow Jones
        dji = yf.Ticker("^DJI")
        dji_price = dji.fast_info['last_price']
        dji_prev_close = dji.fast_info['previous_close']
        dji_change_pct = ((dji_price - dji_prev_close) / dji_prev_close) * 100
        
        result["usd_vnd"] = round(usd_price, 2)
        result["dow_jones"] = {
            "price": round(dji_price, 2),
            "change_pct": round(dji_change_pct, 2)
        }
    except Exception as e:
        logging.error(f"Lỗi khi lấy dữ liệu yfinance: {e}")
        # Quan trọng: Dù lỗi nhưng vẫn trả về cấu trúc dictionary nhất quán
        result["error"] = str(e)
        
    return result
