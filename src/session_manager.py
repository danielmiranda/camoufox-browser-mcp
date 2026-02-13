import hashlib
import os
import uuid
from camoufox import AsyncCamoufox
from playwright.async_api import async_playwright
import asyncio

class SessionManager:
    def __init__(self):
        self.sessions = {}  # hash -> { "browser": browser, "context": context, "page": page }
        self.playwright = None

    async def _ensure_playwright(self):
        if not self.playwright:
            self.playwright = await async_playwright().start()

    async def create_session(self, session_id=None):
        await self._ensure_playwright()
        
        if not session_id:
            session_id = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:12]
        
        # Launch Camoufox
        # Note: Depending on the specific version of camoufox library, 
        # initialization might vary slightly.
        browser = await async_playwright().start() # Placeholder for Camoufox initialization logic
        # For actual camoufox usage with playwright:
        # browser = await Camoufox(headless=True).start() 
        
        # For now, let's use standard playwright as a base, 
        # but the plan is to use Camoufox as requested.
        # Since I'm writing code, I'll aim for the actual camoufox implementation.
        
        # Using camoufox as a context manager or direct launcher
        config = {
            "headless": True,
            "humanize": True
        }
        
        browser = AsyncCamoufox(**config)
        browser_obj = await browser.start()
        context = await browser_obj.new_context()
        page = await context.new_page()
        
        self.sessions[session_id] = {
            "browser": browser_obj,
            "context": context,
            "page": page,
            "camoufox_instance": browser
        }
        
        return session_id

    async def get_session(self, session_id):
        if session_id in self.sessions:
            return self.sessions[session_id]
        return None

    async def list_sessions(self):
        return list(self.sessions.keys())

    async def close_session(self, session_id):
        if session_id in self.sessions:
            session = self.sessions[session_id]
            await session["page"].close()
            await session["context"].close()
            await session["browser"].close()
            del self.sessions[session_id]
            return True
        return False

    async def close_all(self):
        for sid in list(self.sessions.keys()):
            await self.close_session(sid)
