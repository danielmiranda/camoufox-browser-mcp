# Camoufox MCP Browser Server

This is an MCP server that provides stealthy browser automation capabilities using `camoufox` and `FastMCP`.

## Features

- **Anti-Detection**: Powered by Camoufox (custom Firefox).
- **Session Management**: Maintain multiple browser sessions via unique hashes.
- **Dual Screenshot**: Get screenshots via Base64 or save them to the server.
- **Dockerized**: Easy deployment with Docker and Docker Compose.

## Tools

- `browser_navigate`: Navigate to a URL and start/reuse a session.
- `browser_interact`: Click, type, or scroll on a page.
- `browser_screenshot`: Capture the current view.
- `browser_snapshot`: Get the page HTML content.
- `browser_sessions`: List active sessions.

## Quick Start

1. **Build and Run**:
   ```bash
   docker-compose up --build
   ```

2. **Integration with LLM**:
   Configure your MCP client (like Claude Desktop) to connect to the server via stdio:
   ```json
   {
     "mcpServers": {
       "camoufox-browser": {
         "command": "docker",
         "args": ["exec", "-i", "camofox-mcp", "python", "src/mcp_server.py"]
       }
     }
   }
   ```

## Development

- Requirements: `fastmcp`, `camoufox`, `playwright`.
- Python 3.11+ recommended.
