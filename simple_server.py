import http.server
import socketserver
import os
from urllib.parse import urlparse, parse_qs
import mimetypes
from create_windows_zip import create_windows_zip
from create_mac_zip import create_mac_zip
from create_source_zip import create_source_zip

# Configure port
PORT = 5000

# Build game packages
def build_game_packages():
    # Ensure downloads directory exists
    if not os.path.exists('web_static/downloads'):
        os.makedirs('web_static/downloads', exist_ok=True)
    
    # Generate ZIP files
    print("Building Windows package...")
    create_windows_zip()
    print("Building macOS package...")
    create_mac_zip()
    print("Building source code package...")
    create_source_zip()
    print("All game packages built successfully")

class GameWebServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Serve main page
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('web_static/index.html', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Serve download page
        elif path == '/download':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('web_static/download.html', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Serve Windows package download
        elif path == '/download/windows':
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="dodanpyxel-windows.zip"')
            self.end_headers()
            with open('web_static/downloads/dodanpyxel-windows.zip', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Serve macOS package download
        elif path == '/download/mac':
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="dodanpyxel-mac.zip"')
            self.end_headers()
            with open('web_static/downloads/dodanpyxel-mac.zip', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Serve source package download
        elif path == '/download/source':
            self.send_response(200)
            self.send_header('Content-type', 'application/zip')
            self.send_header('Content-Disposition', 'attachment; filename="dodanpyxel-source.zip"')
            self.end_headers()
            with open('web_static/downloads/dodanpyxel-source.zip', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Serve static assets like screenshot
        elif path == '/screenshot.png':
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open('web_static/screenshot.png', 'rb') as file:
                self.wfile.write(file.read())
            return
            
        # Default 404 handler
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 - Not Found')
            return

def main():
    # Build game packages
    build_game_packages()
    
    # Start web server
    handler = GameWebServer
    
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
        print(f"Server started at http://0.0.0.0:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped by user")
        finally:
            httpd.server_close()
            print("Server closed")

if __name__ == "__main__":
    main()