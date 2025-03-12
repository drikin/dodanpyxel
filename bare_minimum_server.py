from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mimetypes

class BareMinimumHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>シューティングゲームダウンロード</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; text-align: center; }
                    h1 { color: #333; }
                    .download-btn { 
                        display: inline-block; 
                        margin: 10px; 
                        padding: 15px 25px; 
                        background-color: #4CAF50; 
                        color: white; 
                        text-decoration: none; 
                        border-radius: 4px;
                        font-size: 18px;
                    }
                    .download-btn:hover { background-color: #45a049; }
                </style>
            </head>
            <body>
                <h1>シューティングゲームダウンロード</h1>
                <p>以下のプラットフォーム用のゲームをダウンロードできます：</p>
                <a href="/download/windows" class="download-btn">Windows版</a>
                <a href="/download/mac" class="download-btn">Mac版</a>
                <a href="/download/source" class="download-btn">ソースコード</a>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path.startswith('/download/'):
            platform = self.path.split('/')[-1]
            filename = None
            
            if platform == 'windows':
                filename = 'dodanpyxel-windows.zip'
            elif platform == 'mac':
                filename = 'dodanpyxel-mac.zip'
            elif platform == 'source':
                filename = 'dodanpyxel-source.zip'
                
            if filename:
                file_path = os.path.join('public', 'downloads', filename)
                
                if os.path.exists(file_path):
                    self.send_response(200)
                    self.send_header('Content-type', 'application/zip')
                    self.send_header('Content-Disposition', f'attachment; filename="{filename}"')
                    self.end_headers()
                    
                    with open(file_path, 'rb') as file:
                        self.wfile.write(file.read())
                else:
                    self.send_response(404)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"File not found")
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Invalid platform")
                
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Server is running")
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"404 Not Found")

def run_server():
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, BareMinimumHandler)
    print(f"Starting bare minimum HTTP server on port 5000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()