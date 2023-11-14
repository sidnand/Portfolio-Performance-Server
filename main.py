import http.server
import socketserver
import json
import os

from sp_sector import get_sp_sector

PORT = 8000

class APIServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/spsector':
            self.send_response(200)
            
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            data = get_sp_sector()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

with socketserver.TCPServer(("", PORT), APIServerHandler) as httpd:
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()