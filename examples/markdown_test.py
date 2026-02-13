import subprocess
import json
import time

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
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()
        
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if line.startswith('{"jsonrpc"'):
                return json.loads(line)
        return None

    def send_notification(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()

    def close(self):
        self.process.terminate()

def main():
    print("--- MCP Markdown Extraction Test ---")
    client = MCPClient()
    
    try:
        # 1. Initialize
        print("\n[H0] Initializing MCP...")
        client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "markdown-test", "version": "1.0.0"}
        })
        client.send_notification("notifications/initialized", {})

        # 2. Open Page
        url = "https://news.ycombinator.com/news"
        print(f"\n[1/3] Opening page: {url}")
        res = client.send_request("tools/call", {
            "name": "browser_navigate", 
            "arguments": {"url": url}
        })
        
        result_text = res["result"]["content"][0]["text"]
        session_id = result_text.split("Session: ")[1].strip()
        print(f"Session started: {session_id}")

        # 3. Get Markdown
        print("\n[2/3] Extracting Markdown...")
        res = client.send_request("tools/call", {
            "name": "browser_get_markdown",
            "arguments": {"session_id": session_id}
        })
        
        markdown_content = res["result"]["content"][0]["text"]
        print("Success! Markdown preview (first 200 chars):")
        print("-" * 40)
        print(markdown_content[:200] + "...")
        print("-" * 40)

        # 4. Save to file
        with open("examples/example_markdown.md", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"\n[3/3] Full markdown saved to 'examples/example_markdown.md'")

    except Exception as e:
        print(f"Test failed: {e}")
    finally:
        client.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    main()
