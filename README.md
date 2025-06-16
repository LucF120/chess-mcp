# chess-mcp

An MCP server that integrates with the public chess.com API 
https://www.chess.com/news/view/published-data-api

Current functions:

<ul>
    <li>get_player_info: Returns basic information about a player from looking up their username (api.chess.com/pub/player/{username})</li>
    <li>get_titled_players: Returns a list of players with a given title (api.chess.com/pub/titled/{title})</li>
    <li>get_player_stats: Returns the stats of a given player (api.chess.com/pub/player/{username}/stats)</li>
</ul>