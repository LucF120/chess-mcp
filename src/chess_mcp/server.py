from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("chess")

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


@mcp.tool()
async def get_player_info(player_name: str) -> str:
    """Get information about a chess player"""
    url = f"{CHESS_API_BASE_URL}player/{player_name}"
    data = await make_chess_request(url)
    
    if not data:
        return "Unable to fetch player data"
    
    data["country"] = await get_country_name(data["country"])
    return format_player_info(data)

@mcp.tool()
async def get_titled_players(title: str) -> str:
    """Get list of titled players with a given title
    Args:
        title: The title of the players to get 
                (e.g. "GM", "WGM", "IM", "WIM", 
                "FM", "WFM", "NM", "WNM", "CM", 
                "WCM")
    """
    valid_titles = ["GM", "WGM", "IM", "WIM", "FM", "WFM", "NM", "WNM", "CM", "WCM"]
    if title not in valid_titles:
        title = convert_title_to_chess_com_format(title)
    url = f"{CHESS_API_BASE_URL}titled/{title}"
    data = await make_chess_request(url)

    if not data:
        return f"Unable to fetch players with the {title} title"
    
    return format_titled_players(data, title)

@mcp.tool()
async def get_player_stats(player_name: str) -> str:
    """Get stats for a chess player"""
    url = f"{CHESS_API_BASE_URL}player/{player_name}/stats"
    data = await make_chess_request(url)
    if not data:
        return f"Unable to fetch stats for {player_name}"
    return format_stats(data, player_name)

async def get_country_name(url: str) -> str:
    """Get the name of a country from its URL"""
    data = await make_chess_request(url)
    if not data:
        return "Unable to fetch country data"
    return data["name"]

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

def format_titled_players(data: dict[str, Any], title: str) -> str:
    """Format the titled players response into a string"""
    return f"""
    Players with the {title} title:
    {", ".join(data["players"])}
    """

def format_game_stats(stats: dict[str, Any]) -> str:
    """Format the game stats into a string"""
    total_games = stats["record"]["win"] + stats["record"]["loss"] + stats["record"]["draw"]
    winrate = stats["record"]["win"] / total_games * 100
    lossrate = stats["record"]["loss"] / total_games * 100
    drawrate = stats["record"]["draw"] / total_games * 100

    return f"""
    Current Rating: {stats["last"]["rating"]}
    Peak Rating: {stats["best"]["rating"]}
    Total Games: {total_games}
    Wins: {stats["record"]["win"]} ({winrate:.2f}%)
    Losses: {stats["record"]["loss"]} ({lossrate:.2f}%)
    Draws: {stats["record"]["draw"]} ({drawrate:.2f}%)
    Date of Peak Rating: {unix_time_to_date(stats["best"]["date"])}
    Game where peak rating was achieved: {stats["best"]["game"]}
    """

def format_tactic_stats(stats: dict[str, Any]) -> str:
    """Format the tactic stats into a string"""
    return f"""
    Peak Tactic Rating: {stats["highest"]["rating"]}
    Date of Peak Tactic Rating: {unix_time_to_date(stats["highest"]["date"])}
    """

def format_puzzle_rush_stats(stats: dict[str, Any]) -> str:
    """Format the puzzle rush stats into a string"""
    return f"""
    Best Puzzle Rush Performance: {stats["best"]["score"]} correct out of {stats["best"]["total_attempts"]}
    """


def format_stats(data: dict[str, Any], player_name: str) -> str:
    """Format the stats response into a string"""
    rapid_stats = data["chess_rapid"]
    blitz_stats = data["chess_blitz"]
    bullet_stats = data["chess_bullet"]
    daily_stats = data["chess_daily"]
    fide_rating = data["fide"]
    tactics_stats = data["tactics"]
    puzzle_rush_stats = data["puzzle_rush"]
    return f"""
    Stats for {player_name}:
    Rapid Stats:
        {format_game_stats(rapid_stats)}
    Blitz Stats:
        {format_game_stats(blitz_stats)}
    Bullet Stats:
        {format_game_stats(bullet_stats)}
    Daily Stats:
        {format_game_stats(daily_stats)}
    Fide Rating:
        {fide_rating}
    Tactics Stats:
        {format_tactic_stats(tactics_stats)}
    Puzzle Rush Stats: 
        {format_puzzle_rush_stats(puzzle_rush_stats)}
    """

def unix_time_to_date(unix_time: int) -> str:
    """Convert a Unix timestamp to a date string"""
    return datetime.fromtimestamp(unix_time).strftime("%Y-%m-%d %H:%M:%S")

def convert_title_to_chess_com_format(title: str) -> str:
    """Convert a title to the format used by the chess.com API"""
    title = title.lower()
    if title == "grandmaster" or title == "gms" or title == "grand master" or title == "grand masters" or title == "grandmasters":
        return "GM"
    elif title == "international master" or title == "ims" or title == "international masters":
        return "IM"
    elif title == "fide master" or title == "fms" or title == "fide masters":
        return "FM"
    elif title == "candidate master" or title == "cms" or title == "candidate masters":
        return "CM"
    elif title == "national master" or title == "nms" or title == "national masters":
        return "NM"
    elif title == "wgm" or title == "w grandmaster" or title == "w grand masters":
        return "WGM"
    elif title == "wim" or title == "w international master" or title == "w international masters":
        return "WIM"
    elif title == "wfm" or title == "w fide master" or title == "w fide masters":
        return "WFM"
    elif title == "wcm" or title == "w candidate master" or title == "w candidate masters":
        return "WCM"
    elif title == "wnm" or title == "w national master" or title == "w national masters":
        return "WNM"   
    else:
        return ""
    
if __name__ == "__main__":
    mcp.run(transport="stdio")