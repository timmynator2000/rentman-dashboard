#!/usr/bin/env python3
"""
Rentman Dashboard Proxy Server
Put this file in the same folder as rentman-dashboard.html
Run: python rentman-proxy.py
Then open: http://localhost:8080/rentman-dashboard.html
"""

import http.server
import urllib.request
import urllib.error
import json
import os
import sys

PORT = 8080
RENTMAN_API = "https://api.rentman.net"
SERVE_DIR = os.path.dirname(os.path.abspath(__file__))


class ProxyHandler(http.server.SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SERVE_DIR, **kwargs)

    def add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Accept, Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self.add_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/"):
            self.proxy_to_rentman()
        else:
            super().do_GET()

    def proxy_to_rentman(self):
        # /api/projects?limit=300  →  strip "/api" (4 chars), keep /projects?limit=300
        rentman_path = self.path[4:]
        url = RENTMAN_API + rentman_path

        auth = self.headers.get("Authorization", "")
        if not auth:
            self._json_response(401, {"error": "No Authorization header"})
            return

        print(f"  → {url}")

        try:
            req = urllib.request.Request(url, headers={
                "Authorization": auth,
                "Accept": "application/json",
                "User-Agent": "RentmanDashboardProxy/1.0",
            })
            with urllib.request.urlopen(req, timeout=20) as resp:
                body = resp.read()
                print(f"  ← {resp.status}  ({len(body)} bytes)")
                self.send_response(resp.status)
                self.add_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

        except urllib.error.HTTPError as e:
            body = e.read()
            print(f"  ← HTTP {e.code}: {body[:300]}")
            self.send_response(e.code)
            self.add_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            print(f"  ← Exception: {e}")
            self._json_response(502, {"error": str(e)})

    def _json_response(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.add_cors_headers()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Only print file-serving lines, not the api proxy lines
        # (proxy lines are printed manually above with more detail)
        if not self.path.startswith("/api/"):
            print("  [file] " + (fmt % args))


if __name__ == "__main__":
    os.chdir(SERVE_DIR)
    print("=" * 54)
    print("  Rentman Dashboard Proxy")
    print("=" * 54)
    print(f"  Folder : {SERVE_DIR}")
    print(f"  API    : {RENTMAN_API}")
    print()
    print(f"  Open in browser:")
    print(f"  http://localhost:{PORT}/rentman-dashboard.html")
    print()
    print("  Press Ctrl+C to stop.")
    print("=" * 54)

    server = http.server.HTTPServer(("", PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Proxy stopped.")
        sys.exit(0)
