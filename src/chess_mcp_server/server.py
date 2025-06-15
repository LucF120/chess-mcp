from mcp.server.fastmcp import FastMCP
from chess_mcp_server.tool_handlers import get_player_info

mcp = FastMCP("chess")

@mcp.tool()
async def get_player_info(player_name: str) -> str:
    """Get information about a chess player"""
    return await get_player_info(player_name)

if __name__ == "__main__":
    mcp.run(transport="stdio")