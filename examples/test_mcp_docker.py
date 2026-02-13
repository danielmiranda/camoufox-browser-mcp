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
            bufsize=1 # Line buffered
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
        
        # Read lines until we find a JSON-RPC response
        while True:
            line = self.process.stdout.readline()
            if not line:
                break
            if line.startswith('{"jsonrpc"'):
                return json.loads(line)
            elif line.strip():
                print(f"SERVER LOG: {line.strip()}")
        return None

    def close(self):
        self.process.terminate()

def main():
    print("--- MCP Docker Persistent Session Test ---")
    client = MCPClient()
    
    try:
        # 1. Initialize
        print("\n[H0] Initializing...")
        res = client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        })
        if not res or "error" in res:
            print(f"Init failed: {res}")
            return
        
        client.send_notification("notifications/initialized", {})
        print("Handshake complete.")

        # 2. List Tools
        print("\n[1/4] Listing tools...")
        res = client.send_request("tools/list", {})
        tools = [t["name"] for t in res["result"]["tools"]]
        print(f"Available tools: {tools}")

        # 3. Navigate
        print("\n[2/4] Navigating to Neuquén...")
        res = client.send_request("tools/call", {
            "name": "browser_navigate", 
            "arguments": {"url": "https://www.neuquen.gob.ar/"}
        })
        if "error" in res:
            print(f"Error: {res['error']}")
            return
            
        result_text = res["result"]["content"][0]["text"]
        session_id = result_text.split("Session: ")[1].strip()
        print(f"Success! Session ID: {session_id}")

        # 4. Screenshot
        print("\n[3/4] Taking screenshot...")
        client.send_request("tools/call", {
            "name": "browser_screenshot",
            "arguments": {
                "session_id": session_id,
                "filename": "persistent_neuquen.png"
            }
        })
        print("Screenshot saved.")

    except Exception as e:
        print(f"Test failed: {e}")
        # Print stderr for debugging
        stderr = client.process.stderr.read()
        if stderr:
            print(f"STDERR: {stderr}")
    finally:
        client.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    main()
