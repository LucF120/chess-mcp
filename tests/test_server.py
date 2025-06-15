import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from chess_mcp_server.server import make_chess_request, get_player_info 

CHESS_API_BASE_URL = "https://api.chess.com/pub/"

@pytest.mark.asyncio
async def test_make_api_request():
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "test_data"}
    mock_response.raise_for_status = MagicMock()
    
    mock_client = MagicMock()
    mock_client.__aenter__.return_value.get.return_value = mock_response
    
    with patch("httpx.AsyncClient", return_value=mock_client):
        result = await make_chess_request("endpoint/test")
        
    assert result == {"data": "test_data"}
    mock_client.__aenter__.return_value.get.assert_called_once()
    url_called = mock_client.__aenter__.return_value.get.call_args[0][0]
    assert url_called == f"{CHESS_API_BASE_URL}/endpoint/test"

@pytest.mark.asyncio
async def test_get_player_profile():
    mock_data = {"username": "testuser", "avatar": "test_url", "status": "active"}
    with patch("chess_mcp.server.make_api_request", new=AsyncMock(return_value=mock_data)):
        result = await get_player_info("testuser")
    
    assert result == mock_data