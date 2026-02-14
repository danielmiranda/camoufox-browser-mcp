import subprocess
import json
import base64
import os
import time

class MCPClient:
    def __init__(self):
        # We assume the container 'camofox-mcp' is running
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
        print(f"DEBUG: Sending request {self.msg_id} - {method}")
        self.msg_id += 1
        self.process.stdin.write(json.dumps(payload) + "\n")
        self.process.stdin.flush()
        
        # Read until we find our response ID
        start_time = time.time()
        while time.time() - start_time < 30: # 30 second timeout
            line = self.process.stdout.readline()
            if not line:
                print("DEBUG: No more stdout lines")
                break
            
            line = line.strip()
            if not line:
                continue
            
            print(f"DEBUG: Received line: {line[:100]}...")
            
            try:
                data = json.loads(line)
                if data.get("id") == payload["id"]:
                    return data
            except json.JSONDecodeError:
                continue
                
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
    print("--- MCP Screenshot Format Test (Improved) ---")
    client = MCPClient()
    
    try:
        # 1. Initialize
        print("\n[1/3] Initializing MCP...")
        res = client.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "screenshot-test", "version": "1.0.0"}
        })
        
        if not res:
            print("❌ Initialization failed (no response)")
            return

        client.send_notification("notifications/initialized", {})

        # 2. Open Page
        url = "https://www.google.com"
        print(f"\n[2/3] Opening page: {url}")
        res = client.send_request("tools/call", {
            "name": "browser_navigate", 
            "arguments": {"url": url}
        })
        
        if not res or "result" not in res:
            print(f"❌ Navigation failed. Response: {res}")
            return

        result_text = res["result"]["content"][0]["text"]
        if "Session: " not in result_text:
            print(f"❌ Could not find session in result: {result_text}")
            return
            
        session_id = result_text.split("Session: ")[1].strip()
        print(f"Session started: {session_id}")

        # 3. Take Screenshot
        print("\n[3/3] Taking screenshot...")
        res = client.send_request("tools/call", {
            "name": "browser_screenshot",
            "arguments": {"session_id": session_id}
        })
        
        if not res or "result" not in res:
            print(f"❌ Screenshot failed. Response: {res}")
            return

        # Verify the result format
        content = res["result"]["content"]
        found_image = False
        for item in content:
            if item.get("type") == "image":
                found_image = True
                print("✅ Success! Resource identified as 'image'.")
                print(f"   MIME Type: {item.get('mimeType')}")
                
                # Save the image to disk to verify it's valid
                img_data = item.get("data")
                if img_data:
                    output_file = "examples/test_screenshot.png"
                    with open(output_file, "wb") as f:
                        f.write(base64.b64decode(img_data))
                    print(f"   Image saved to: {output_file}")
                break
        
        if not found_image:
            print("❌ Error: No image resource found in the response.")
            print(f"   Response content: {json.dumps(content, indent=2)}")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\n--- Done ---")

if __name__ == "__main__":
    main()
