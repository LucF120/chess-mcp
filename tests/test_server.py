import pytest
from unittest.mock import patch, AsyncMock
from chess_mcp.server import get_player_info

@pytest.mark.asyncio
async def test_get_player_profile():
    # Mock data with all required fields
    mock_data = {
        "username": "testuser",
        "url": "https://www.chess.com/member/testuser",
        "country": "https://api.chess.com/pub/country/US",
        "joined": 1342890655,
        "last_online": 1718460000,
        "status": "premium",
        "is_streamer": False,
        "league": "Legend"
    }
    
    # Mock both the chess request and country request
    with patch("chess_mcp.tools.handlers.make_chess_request") as mock_request:
        # First call returns player data, second call returns country data
        mock_request.side_effect = [
            mock_data,  # Player data
            {"name": "United States"}  # Country data
        ]
        
        result = await get_player_info("testuser")
    
    # Check that the result is a formatted string containing expected data
    assert "Player: testuser" in result
    assert "URL: https://www.chess.com/member/testuser" in result
    assert "Country: United States" in result
    assert "Status: premium" in result
    assert "League: Legend" in result