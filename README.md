# 🦊 Camoufox MCP Browser

[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-blue)](https://modelcontextprotocol.io)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)](https://www.python.org/)

A **Model Context Protocol (MCP)** server designed to provide stealthy web browsing capabilities (anti-detection) to AI agents using the **Camoufox** engine.

## 🚀 Goal
Enable AI agents (such as Claude, GPT, etc.) to interact with the modern web without being blocked, maintaining persistent sessions and allowing detailed visual and structural inspection of content.

## ✨ Key Features

- **🕵️ Advanced Stealth**: Engine based on Camoufox (custom Firefox) with C++ level fingerprint spoofing.
- **🔗 Session Management**: Hash-based system to maintain multiple independent and persistent navigation contexts.
- **📸 Dual Screenshots**: Returns screenshots in Base64 directly to the agent and optionally saves them to local files.
- **🛠️ Interaction Tools**: Navigation, clicks, text typing, scrolling, and link extraction.
- **🐳 Docker Native**: Optimized container with all necessary system dependencies to run browsers in headless mode.

## 🛠️ Available Tools

| Tool | Description |
| :--- | :--- |
| `browser_navigate` | Navigates to a URL and creates/reuses a persistent session. |
| `browser_interact` | Performs actions like `click`, `type`, `scroll_up`, `scroll_down`. |
| `browser_list_links`| Extracts all links and their descriptive text from the current page. |
| `browser_screenshot`| Captures the current view (Base64 + optional file). |
| `browser_snapshot` | Retrieves the raw HTML content of the session. |
| `browser_sessions` | Lists the hashes of all active sessions. |

## 📦 Installation and Usage

### 1. Requirements
- Docker and Docker Compose.
- Python 3.11+ (to run test scripts).

### 2. Deployment with Docker
```bash
# Clone and start
git clone https://github.com/danielmiranda/camoufox-browser-mcp.git
cd camoufox-browser-mcp
docker-compose up --build -d
```

### 3. Configuration in MCP Clients (e.g., Claude Desktop)
Add the following to your configuration file:
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

## 🧪 Verification Tests

We have included example scripts to verify integration:
- **General Test**: `python examples/test_mcp_docker.py` (Simulates full agent flow).
- **ScrapingBee Test**: `python examples/scrapingbee_test.py` (Navigates, lists links, and performs clicks).

## ⚠️ Current Limitations

- **Resource Consumption**: Since it manages persistent sessions, memory usage can scale with many open tabs.
- **Headless Mode**: Some websites specifically detect headless rendering despite advanced spoofing (though Camoufox minimizes this).
- **Network**: Loading speed depends entirely on the Docker host's connectivity.

## 🗺️ Roadmap (Future)

- [ ] **AI-Optimized Markdown**: Tool to extract web content directly as Markdown (token saving).
- [ ] **Accessibility Tree tools**: Tools to interact based on accessibility roles instead of CSS selectors.
- [ ] **Proxy Rotation**: Integrated proxy management for each hashed session.
- [ ] **Captcha Solving**: Integration with captcha solving services for fully autonomous flows.

---
Built with ❤️ for the AI Agent community.
