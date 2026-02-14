import os
import base64
import asyncio
from markdownify import markdownify as md
from fastmcp import FastMCP
from fastmcp.utilities.types import Image
from session_manager import SessionManager

# Initialize FastMCP server
mcp = FastMCP("Camoufox Browser")
manager = SessionManager()

SCREENSHOT_PATH = os.environ.get("SCREENSHOT_PATH", "./screenshots")
if not os.path.exists(SCREENSHOT_PATH):
    os.makedirs(SCREENSHOT_PATH)

@mcp.tool()
async def browser_navigate(url: str, session_id: str = None) -> str:
    """Navigate to a URL. Returns the session_id used."""
    if not session_id:
        session_id = await manager.create_session()
    
    session = await manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found."
    
    await session["page"].goto(url)
    return f"Navigated to {url}. Session: {session_id}"

@mcp.tool()
async def browser_interact(session_id: str, action: str, selector: str = None, text: str = None) -> str:
    """
    Interact with the browser.
    Actions: click, type, scroll_down, scroll_up
    """
    session = await manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found."
    
    page = session["page"]
    
    if action == "click":
        await page.click(selector)
        return f"Clicked {selector}"
    elif action == "type":
        await page.fill(selector, text)
        return f"Typed '{text}' into {selector}"
    elif action == "scroll_down":
        await page.evaluate("window.scrollBy(0, 500)")
        return "Scrolled down"
    elif action == "scroll_up":
        await page.evaluate("window.scrollBy(0, -500)")
        return "Scrolled up"
    else:
        return f"Unknown action: {action}"

@mcp.tool()
async def browser_screenshot(session_id: str, filename: str = None) -> Image:
    """
    Capture a screenshot.
    Returns an Image object (recognized as image resource).
    """
    session = await manager.get_session(session_id)
    if not session:
        raise ValueError(f"Session {session_id} not found.")
    
    page = session["page"]
    
    # Take screenshot as bytes
    screenshot_bytes = await page.screenshot()
    
    if filename:
        full_path = os.path.join(SCREENSHOT_PATH, filename)
        with open(full_path, "wb") as f:
            f.write(screenshot_bytes)
    
    return Image(data=screenshot_bytes, format="png")

@mcp.tool()
async def browser_list_links(session_id: str) -> list:
    """List all links (href) on the current page."""
    session = await manager.get_session(session_id)
    if not session:
        return [f"Error: Session {session_id} not found."]
    
    page = session["page"]
    links = await page.eval_on_selector_all("a", "elements => elements.map(e => ({ text: e.innerText, href: e.href }))")
    return links

@mcp.tool()
async def browser_get_markdown(session_id: str) -> str:
    """Get the current page content as Markdown."""
    session = await manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found."
    
    html = await session["page"].content()
    return md(html, heading_style="ATX")

@mcp.tool()
async def browser_snapshot(session_id: str) -> str:
    """Get the current page content (HTML)."""
    session = await manager.get_session(session_id)
    if not session:
        return f"Error: Session {session_id} not found."
    
    return await session["page"].content()

@mcp.tool()
async def browser_sessions() -> list:
    """List all active session IDs."""
    return await manager.list_sessions()

if __name__ == "__main__":
    mcp.run()
