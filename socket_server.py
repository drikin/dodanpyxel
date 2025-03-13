import socket
import os
import threading

# シンプルなHTTPレスポンス作成関数
def create_http_response(status_code, content_type, body):
    header = f"HTTP/1.1 {status_code}\r\n"
    header += f"Content-Type: {content_type}\r\n"
    header += f"Content-Length: {len(body)}\r\n"
    header += "\r\n"
    return header.encode() + body

def handle_client(client_socket):
    # リクエスト受信
    request_data = client_socket.recv(4096).decode('utf-8')
    
    # リクエストデータの最初の行からパスを抽出
    first_line = request_data.split('\n')[0]
    path = first_line.split(' ')[1]
    
    # ルーティング処理
    if path == '/':
        # メインページHTML
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
        response = create_http_response(200, "text/html", html.encode())
        client_socket.send(response)
    
    # ヘルスチェック用エンドポイント
    elif path == '/health':
        response = create_http_response(200, "text/plain", b"Server is running")
        client_socket.send(response)
        
    # ダウンロードエンドポイント
    elif path.startswith('/download/'):
        platform = path.split('/')[-1]
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
                with open(file_path, 'rb') as file:
                    file_content = file.read()
                    
                # コンテンツタイプとダウンロード用ヘッダーを設定
                headers = f"HTTP/1.1 200 OK\r\n"
                headers += f"Content-Type: application/zip\r\n"
                headers += f"Content-Disposition: attachment; filename=\"{filename}\"\r\n"
                headers += f"Content-Length: {len(file_content)}\r\n"
                headers += "\r\n"
                
                client_socket.send(headers.encode() + file_content)
            else:
                response = create_http_response(404, "text/html", b"File not found")
                client_socket.send(response)
        else:
            response = create_http_response(400, "text/html", b"Invalid platform")
            client_socket.send(response)
            
    else:
        response = create_http_response(404, "text/html", b"404 Not Found")
        client_socket.send(response)
    
    # ソケットを閉じる
    client_socket.close()

def start_server():
    # ソケットを作成
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # ポートバインド
    server_address = ('0.0.0.0', 5000)
    print(f"Starting socket server on {server_address[0]}:{server_address[1]}...")
    server.bind(server_address)
    
    # 接続待ち
    server.listen(5)
    print("Server is listening for connections...")
    
    try:
        # 接続を受け付け、スレッドでハンドリング
        while True:
            client, address = server.accept()
            print(f"Connection from {address}")
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.daemon = True
            client_handler.start()
    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()