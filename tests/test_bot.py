import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Note: We will implement bot.py later. We're writing the test first (TDD).
# We assume there is a function handle_start_command in bot.py
# and a function handle_chat_message in bot.py

@pytest.mark.asyncio
@patch("bot.check_chat_id", return_value=True)
async def test_handle_start_command(mock_check_chat_id):
    from bot import handle_start_command
    
    # Mock message
    message = AsyncMock()
    
    await handle_start_command(message)
    
    # Verify the bot sends a welcome message
    message.answer.assert_called_once()
    args, _ = message.answer.call_args
    assert "Xin chào" in args[0] or "Trading Mentor" in args[0]

@pytest.mark.asyncio
@patch("bot.app")
@patch("bot.check_chat_id", return_value=True)
async def test_handle_chat_message(mock_check_chat_id, mock_app):
    from bot import handle_chat_message
    
    # Mock message
    message = AsyncMock()
    message.text = "Thị trường hôm nay thế nào?"
    
    # Mock graph app invoke response
    mock_app.invoke = MagicMock(return_value={"final_response": "Thị trường đang tốt."})
    
    await handle_chat_message(message)
    
    # Verify graph is invoked with correct trigger
    mock_app.invoke.assert_called_once()
    args, _ = mock_app.invoke.call_args
    assert args[0]["trigger_type"] == "chat"
    assert args[0]["user_intent"] == "Thị trường hôm nay thế nào?"
    
    # Verify response is sent back to user
    message.answer.assert_called_once_with("Thị trường đang tốt.")
