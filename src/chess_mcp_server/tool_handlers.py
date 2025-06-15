# tools/tool_handlers.py
from typing import Any
import httpx
from util import unix_time_to_date

CHESS_API_BASE_URL = "https://api.chess.com/pub/"
USER_AGENT = "chess-mcp-server/1.0"

async def make_chess_request(url: str) -> dict[str, Any] | None:
    """Make a request to the chess API"""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_player_info(data: dict[str, Any]) -> str:
    """Format the profile response into a string"""
    return f"""
    Player: {data["username"]}
    URL: {data["url"]}
    Country: {data["country"]}
    Joined: {data["joined"]}
    Last Online: {unix_time_to_date(data["last_online"])}
    Status: {data["status"]}
    Is Streamer: {data["is_streamer"]}
    League: {data["league"]}
    """

async def get_player_info(player_name: str) -> str:
    """Get information about a chess player"""
    url = f"{CHESS_API_BASE_URL}player/{player_name}"
    data = await make_chess_request(url)
    
    if not data:
        return "Unable to fetch player data"
    
    data["country"] = await get_country_name(data["country"])
    return format_player_info(data)

async def get_country_name(url: str) -> str:
    """Get the name of a country from its URL"""
    data = await make_chess_request(url)
    if not data:
        return "Unable to fetch country data"
    return data["name"]