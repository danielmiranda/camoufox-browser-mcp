import pytest
import asyncio
import os
from src.session_manager import SessionManager

@pytest.mark.asyncio
async def test_session_lifecycle():
    manager = SessionManager()
    session_id = await manager.create_session()
    assert session_id is not None
    assert len(await manager.list_sessions()) == 1
    
    success = await manager.close_session(session_id)
    assert success is True
    assert len(await manager.list_sessions()) == 0

@pytest.mark.asyncio
async def test_navigation():
    manager = SessionManager()
    session_id = await manager.create_session()
    session = await manager.get_session(session_id)
    page = session["page"]
    
    await page.goto("https://example.com")
    title = await page.title()
    assert "Example Domain" in title
    
    await manager.close_session(session_id)
