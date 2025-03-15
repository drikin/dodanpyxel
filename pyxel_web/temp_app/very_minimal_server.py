import http.server
import socketserver
import os

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public", **kwargs)

if __name__ == "__main__":
    PORT = 5000
    
    print(f"Starting very minimal HTTP server on port {PORT}...")
    print(f"Serving files from the 'public' directory...")
    print(f"Try accessing: http://localhost:{PORT}/")
    
    with socketserver.TCPServer(("0.0.0.0", PORT), MyHandler) as httpd:
        print("Server started. Press Ctrl+C to stop.")
        httpd.serve_forever()