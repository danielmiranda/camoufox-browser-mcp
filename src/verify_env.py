import asyncio
from camoufox import AsyncCamoufox
import sys

async def verify():
    print("Verifying browser environment...")
    try:
        config = {
            "headless": True,
            "humanize": True
        }
        print("Launching AsyncCamoufox...")
        browser = AsyncCamoufox(**config)
        browser_obj = await browser.start()
        print("Browser started successfully.")
        
        context = await browser_obj.new_context()
        page = await context.new_page()
        print("Context and Page created.")
        
        url = "https://example.com"
        print(f"Navigating to {url}...")
        await page.goto(url, timeout=30000)
        title = await page.title()
        print(f"Success! Page title: {title}")
        
        await browser_obj.close()
        print("Browser closed.")
        return True
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(verify())
    sys.exit(0 if success else 1)
