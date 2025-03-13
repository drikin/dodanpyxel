from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>テストサーバー</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
                background-color: #333;
                color: white;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #444;
                border-radius: 10px;
            }
            h1 {
                color: #ffcc00;
            }
            .btn {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin: 10px 0;
                border-radius: 5px;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Replit Webview テスト</h1>
            <p>このサーバーは正常に動作しています。</p>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("Starting test server...")
    app.run(host='0.0.0.0', port=5000)