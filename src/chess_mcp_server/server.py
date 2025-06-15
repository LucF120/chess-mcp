from mcp.server.fastmcp import FastMCP
import tool_handlers as tools

mcp = FastMCP("chess")

@mcp.tool()
async def get_player_info(player_name: str) -> str:
    """Get information about a chess player"""
    return await tools.get_player_info(player_name)

if __name__ == "__main__":
    mcp.run(transport="stdio")