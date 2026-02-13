import subprocess
import json
import sys
import time
import os

class MCPClient:
    def __init__(self):
        cmd = ["docker", "exec", "-i", "camofox-mcp", "python", "src/mcp_server.py"]
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        self.msg_id = 1

    def send_request(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": self.msg_id,
            "method": method,
            "params": params
        }
        self.msg_id += 1
        return self._send(payload)

    def send_notification(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()

    def _send(self, payload):
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()
        
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if line.startswith('{"jsonrpc"'):
                return json.loads(line)
        return None

    def close(self):
        self.process.terminate()

def main():
    print("--- ScrapingBee Blog Traversal Test ---")
    client = MCPClient()
    
    try:
        # 1. Initialize
        print("\n[H0] Initializing MCP...")
        client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "scrapingbee-test", "version": "1.0.0"}
        })
        client.send_notification("notifications/initialized", {})

        # 2. Open Page
        url = "https://www.scrapingbee.com/blog/how-to-scrape-with-camoufox-to-bypass-antibot-technology/"
        print(f"\n[1/5] Opening ScrapingBee blog: {url}")
        res = client.send_request("tools/call", {
            "name": "browser_navigate", 
            "arguments": {"url": url}
        })
        
        result_text = res["result"]["content"][0]["text"]
        session_id = result_text.split("Session: ")[1].strip()
        print(f"Session started: {session_id}")

        # 3. List Links
        print("\n[2/5] Listing available links...")
        res = client.send_request("tools/call", {
            "name": "browser_list_links",
            "arguments": {"session_id": session_id}
        })
        
        links = json.loads(res["result"]["content"][0]["text"])
        print(f"Found {len(links)} links. Top 5:")
        for i, link in enumerate(links[:5]):
            print(f"{i+1}. {link['text']} -> {link['href']}")

        # 4. First Screenshot
        print("\n[3/5] Taking first screenshot...")
        client.send_request("tools/call", {
            "name": "browser_screenshot",
            "arguments": {
                "session_id": session_id,
                "filename": "scrapingbee_1_initial.png"
            }
        })
        print("Saved: screenshots/scrapingbee_1_initial.png")

        # 5. Click First Link
        first_link_selector = "a" # Clicking the first 'a' tag as a simple test
        print(f"\n[4/5] Clicking the first link: {links[0]['text']}")
        client.send_request("tools/call", {
            "name": "browser_interact",
            "arguments": {
                "session_id": session_id,
                "action": "click",
                "selector": "a" # We'll just use the generic 'a' selector for the first match
            }
        })
        print("Waiting for navigation...")
        time.sleep(3) # Wait a bit for the page to load

        # 6. Second Screenshot
        print("\n[5/5] Taking final screenshot...")
        client.send_request("tools/call", {
            "name": "browser_screenshot",
            "arguments": {
                "session_id": session_id,
                "filename": "scrapingbee_2_after_click.png"
            }
        })
        print("Saved: screenshots/scrapingbee_2_after_click.png")

    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        client.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    main()
