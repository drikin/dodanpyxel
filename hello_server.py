from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hello World</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background-color: #f0f0f0;
                    margin: 0;
                }
                .container {
                    text-align: center;
                    padding: 20px;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #333;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Hello World!</h1>
                <p>This is a simple test page.</p>
                <p>If you can see this, the web server is working!</p>
            </div>
        </body>
        </html>
        """)

def run_server():
    server_address = ('0.0.0.0', 5000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f'Starting server on port {server_address[1]}...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('Server stopped by user')
    finally:
        httpd.server_close()
        print('Server closed')

if __name__ == '__main__':
    run_server()