import socket
import threading

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    
    # Create simple HTTP response
    response = "HTTP/1.1 200 OK\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Ultra Basic Server</title>
    </head>
    <body>
        <h1>Hello World</h1>
        <p>This is served from the most basic Python socket server possible.</p>
        <p>If you see this, the server is working!</p>
    </body>
    </html>
    """
    
    client_socket.send(response.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    
    print(f"[*] Listening on 0.0.0.0:5000")
    
    while True:
        client, addr = server.accept()
        print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()