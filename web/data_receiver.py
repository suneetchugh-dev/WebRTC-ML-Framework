#!/usr/bin/env python3
"""
WebRTC Diagnostics Telemetry Ingestion Receiver
Collects empirical getStats() diagnostic traces from web/index.html and writes to data/raw.
Cross-platform compatible (Linux/Windows/macOS) with strict path traversal defenses.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import re
import sys
from datetime import datetime

# Resolve project base directory relative to this script:
# __file__ -> Research-Project/web/data_receiver.py
# parent -> Research-Project/web
# grandparent -> Research-Project
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
RAW_DIR = os.environ.get("WEBRTC_RAW_DIR", os.path.join(PROJECT_DIR, "data", "raw"))
os.makedirs(RAW_DIR, exist_ok=True)


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_POST(self):
        if self.path == '/save':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))

                # Sanitize input tokens to prevent path traversal
                raw_run_id = str(data.get('run_id', 'unknown'))
                raw_label = str(data.get('label', 'unknown'))
                run_id = re.sub(r'[^a-zA-Z0-9_-]', '', raw_run_id) or 'run_001'
                label = re.sub(r'[^a-zA-Z0-9_-]', '', raw_label) or 'normal'
                csv_content = data.get('csv', '')
                rows_count = data.get('rows', 0)

                timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{run_id}_{label}_{timestamp_str}.csv"
                filepath = os.path.abspath(os.path.join(RAW_DIR, filename))

                # Security Assertion: Ensure destination path stays strictly within RAW_DIR
                if not filepath.startswith(os.path.abspath(RAW_DIR)):
                    self._set_headers(403)
                    self.wfile.write(json.dumps({'error': 'Access denied: Path traversal detected'}).encode('utf-8'))
                    return

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(csv_content)

                print(f"[INGESTION SUCCESS] {filename} ({rows_count} records committed to {RAW_DIR})")
                self._set_headers(200)
                self.wfile.write(json.dumps({
                    'status': 'ok',
                    'file': filename,
                    'rows': rows_count,
                    'directory': RAW_DIR
                }).encode('utf-8'))

            except Exception as e:
                print(f"[INGESTION ERROR] {str(e)}", file=sys.stderr)
                self._set_headers(500)
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))

    def log_message(self, format, *args):
        # Suppress routine server polling logs to keep terminal diagnostics stream clean
        pass


def run_server(port=8002):
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, Handler)
    print(f"============================================================")
    print(f" WebRTC Telemetry Data Ingestion Daemon Active")
    print(f" Listening on: http://127.0.0.1:{port}/save")
    print(f" Storage Directory: {RAW_DIR}")
    print(f" Cross-Platform & Path Traversal Protections: ENFORCED")
    print(f"============================================================")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ingestion server gracefully...")
        httpd.server_close()


if __name__ == '__main__':
    run_server()
