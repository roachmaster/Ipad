from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import time
import os

TOKEN = os.environ.get("AGENT_TOKEN", "change-me")
REPO = "/root/workspace/Ipad"

ALLOWED = {
    "info": ["sh", f"{REPO}/agent/scripts/info.sh"],
    "hello": ["sh", f"{REPO}/agent/scripts/hello.sh"],
    "bitwave": ["python3", f"{REPO}/bitwave/bitwave.py"],
}

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/run":
            self._send(404, {"error": "not found"})
            return

        if self.headers.get("X-Agent-Token") != TOKEN:
            self._send(403, {"error": "denied"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        data = json.loads(self.rfile.read(length) or b"{}")
        job = data.get("job")

        if job not in ALLOWED:
            self._send(400, {"error": "job not allowed", "allowed": list(ALLOWED)})
            return

        subprocess.run(["git", "-C", REPO, "pull", "origin", "main"], capture_output=True, text=True)

        start = time.time()
        result = subprocess.run(ALLOWED[job], capture_output=True, text=True, timeout=60)

        self._send(200, {
            "job": job,
            "returncode": result.returncode,
            "seconds": round(time.time() - start, 3),
            "stdout": result.stdout,
            "stderr": result.stderr
        })

HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
