import pytest
from unittest.mock import patch, AsyncMock
from chess_mcp.server import make_chess_request, get_player_info, get_titled_players, get_player_stats

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
    with patch("chess_mcp.server.make_chess_request") as mock_request:
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

@pytest.mark.asyncio
async def test_get_titled_players():
    # Mock data with titled players
    mock_data = {
        "title": "GM",
        "players": ["testuser1", "testuser2", "testuser3"]
    }
    
    # Mock the chess request
    with patch("chess_mcp.server.make_chess_request") as mock_request:
        mock_request.return_value = mock_data

        result = await get_titled_players("Grandmaster")

    # Check that the result is a formatted string containing expected data
    assert "Players with the GM title" in result
    assert "testuser1, testuser2, testuser3" in result

@pytest.mark.asyncio
async def test_get_player_stats():
    # Mock data with player stats
    mock_data = {
        "chess_daily": {
            "last": {
            "rating": 1472,
            "date": 1739845268,
            "rd": 115
            },
            "best": {
            "rating": 1472,
            "date": 1736997738,
            "game": "https://www.chess.com/game/daily/524136419"
            },
            "record": {
            "win": 98,
            "loss": 31,
            "draw": 3,
            "time_per_move": 10652,
            "timeout_percent": 0
            }
        },
        "chess_rapid": {
            "last": {
            "rating": 2071,
            "date": 1748742005,
            "rd": 49
            },
            "best": {
            "rating": 2164,
            "date": 1733774324,
            "game": "https://www.chess.com/game/live/127425079561"
            },
            "record": {
            "win": 1599,
            "loss": 1464,
            "draw": 149
            }
        },
        "chess_bullet": {
            "last": {
            "rating": 1879,
            "date": 1750031890,
            "rd": 18
            },
            "best": {
            "rating": 2235,
            "date": 1737919205,
            "game": "https://www.chess.com/game/live/87663077945"
            },
            "record": {
            "win": 9052,
            "loss": 9530,
            "draw": 1130
            }
        },
        "chess_blitz": {
            "last": {
            "rating": 2007,
            "date": 1746369963,
            "rd": 32
            },
            "best": {
            "rating": 2150,
            "date": 1687796776,
            "game": "https://www.chess.com/game/live/124303746697"
            },
            "record": {
            "win": 8830,
            "loss": 9209,
            "draw": 948
            }
        },
        "fide": 1374,
        "tactics": {
            "highest": {
            "rating": 3025,
            "date": 1717789546
            },
            "lowest": {
            "rating": 928,
            "date": 1614109275
            }
        },
        "puzzle_rush": {
            "best": {
            "total_attempts": 58,
            "score": 55
            }
        }
    }

    with patch("chess_mcp.server.make_chess_request") as mock_request:
        mock_request.return_value = mock_data

        result = await get_player_stats("testuser")

    # Check that the result is a formatted string containing expected data
    assert "Stats for testuser" in result
    assert "Rapid Stats" in result
    assert "Blitz Stats" in result
    assert "Bullet Stats" in result
    assert "Daily Stats" in result
    assert "Fide Rating" in result
    assert "Tactics Stats" in result
    assert "Puzzle Rush Stats" in result
    assert "1472" in result
    assert "2164" in result
    assert "2071" in result
    assert "1879" in result
    assert "2007" in result
    assert "1374" in result
    assert "3025" in result
    assert "55" in result