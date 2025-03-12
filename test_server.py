from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>シューティングゲーム - テストページ</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                text-align: center;
                padding: 20px;
            }
            h1 {
                color: #333;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>テストページが表示されました！</h1>
            <p>Webサーバーが正常に動作しています。</p>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("Starting test server...")
    app.run(host='0.0.0.0', port=5000)