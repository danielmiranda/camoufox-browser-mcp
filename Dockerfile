FROM python:3.11-bullseye

# Install comprehensive dependencies for Firefox/Playwright
RUN apt-get update && apt-get install -y \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxt6 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgbm1 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libxrender1 \
    libxshmfence1 \
    libglu1-mesa \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Camoufox setup
RUN python -m camoufox fetch

COPY src/ ./src/
COPY README.md .

# Create screenshots directory
RUN mkdir -p /app/screenshots

ENV PYTHONUNBUFFERED=1
ENV SCREENSHOT_PATH=/app/screenshots

# Command to run the MCP server
CMD ["python", "src/mcp_server.py"]
