import pytest
from utils import format_for_telegram

def test_format_for_telegram_basic():
    text = "**Bold** and *italic* and `code`."
    expected = "<b>Bold</b> and <i>italic</i> and <code>code</code>."
    assert format_for_telegram(text) == expected

def test_format_for_telegram_links():
    text = "Check [Google](https://google.com)"
    expected = 'Check <a href="https://google.com">Google</a>'
    assert format_for_telegram(text) == expected

def test_format_for_telegram_headers():
    text = "## Tiêu đề chính\nNội dung"
    expected = "<b>Tiêu đề chính</b>\nNội dung"
    assert format_for_telegram(text) == expected

def test_format_for_telegram_escape_html():
    text = "Giá < 100 và > 50"
    # Dấu < > phải được escape trước, tránh lỗi HTML parse của Telegram
    expected = "Giá &lt; 100 và &gt; 50"
    assert format_for_telegram(text) == expected
