from mcp.server.fastmcp import FastMCP
from tools.tool_handlers import get_player_data

mcp = FastMCP("chess")

@mcp.tool()
async def get_player_info(player_name: str) -> str:
    """Get information about a chess player"""
    return await get_player_data(player_name)

if __name__ == "__main__":
    mcp.run(transport="stdio")