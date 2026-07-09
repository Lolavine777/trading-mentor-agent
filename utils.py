import re

def format_for_telegram(text: str) -> str:
    """
    Chuyển đổi chuẩn Markdown của LLM (Gemini) sang định dạng HTML được Telegram hỗ trợ.
    Telegram HTML chỉ hỗ trợ các tag: <b>, <i>, <u>, <s>, <a>, <code>, <pre>
    """
    if not text:
        return ""
        
    # 1. Escape HTML special characters first (tránh lỗi parse HTML của Telegram)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # 2. Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text, flags=re.DOTALL)
    
    # 3. Italic: *text* -> <i>text</i>
    # Tránh dính vào dấu ** đã xử lý ở trên
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text, flags=re.DOTALL)
    
    # 4. Code: `text` -> <code>text</code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text, flags=re.DOTALL)
    
    # 5. Links: [text](url) -> <a href="url">text</a>
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # 6. Headers: ## Header -> <b>Header</b> (Vì Telegram không hỗ trợ tag h1, h2, h3)
    text = re.sub(r'^#{1,6}\s+(.*)$', r'<b>\1</b>', text, flags=re.MULTILINE)
    
    return text
