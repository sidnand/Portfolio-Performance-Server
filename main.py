import http.server
import socketserver
import json
import os
from ken_r_french import *

from sp_sector import get_sp_sector

PORT = 8000

class APIServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
            
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/spsector':            
            data = get_sp_sector()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/25_1':
            data = get_25_1()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/25_3':
            data = get_25_3()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/25_4':
            pass
        elif self.path == '/ff4':
            data = get_3_factors()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/industry':
            data = get_10_industry_riskfree()
            self.wfile.write(json.dumps(data).encode())

        elif self.path == '/international':
            pass
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

with socketserver.TCPServer(("", PORT), APIServerHandler) as httpd:
    if not os.path.exists('data'):
        os.makedirs('data')
    
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()