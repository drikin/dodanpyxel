from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import subprocess

# First run the packaging scripts to generate the ZIP files
def build_game_packages():
    # Create downloads directory if it doesn't exist
    if not os.path.exists('web_static/downloads'):
        os.makedirs('web_static/downloads', exist_ok=True)
    
    # Build packages
    try:
        subprocess.run([sys.executable, 'create_windows_zip.py'], check=True)
        subprocess.run([sys.executable, 'create_mac_zip.py'], check=True)
        subprocess.run([sys.executable, 'create_source_zip.py'], check=True)
        print("All game packages built successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error building game packages: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Simple HTTP server that serves files from the web_static directory
class GameWebServer(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='web_static', **kwargs)

# Main function that starts the server
def main():
    # Build packages first
    build_game_packages()
    
    # Set up HTTP server on port 5000
    port = 5000
    server_address = ('', port)
    
    # Create and start HTTP server
    httpd = HTTPServer(server_address, GameWebServer)
    print(f"Starting web server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    main()