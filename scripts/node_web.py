"""Loopback-only HTTP view of the one running node sampler."""

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from threading import Thread


class WebDashboard:
    def __init__(self, port):
        page = Path(__file__).with_name("node-activity.html").read_bytes()
        self.publish({"at": None, "status": "Waiting for first snapshot", "nodes": []})
        view = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                host = self.headers.get("Host", "").partition(":")[0].lower()
                if host not in ("localhost", "127.0.0.1") and not host.endswith(".ts.net"):
                    self.send_error(403)
                    return
                if self.path == "/":
                    body, mime = page, "text/html"
                elif self.path == "/snapshot":
                    body, mime = view.body, "application/json"
                else:
                    self.send_error(404)
                    return
                self.send_response(200)
                self.send_header("Content-Type", mime + "; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("X-Content-Type-Options", "nosniff")
                self.send_header("X-Frame-Options", "DENY")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
        Thread(target=self.server.serve_forever, daemon=True).start()

    def publish(self, snapshot):
        self.body = json.dumps(snapshot, allow_nan=False, separators=(",", ":")).encode()

    def close(self):
        self.server.shutdown()
        self.server.server_close()
