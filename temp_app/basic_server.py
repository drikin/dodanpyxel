from flask import Flask, send_file, render_template_string, send_from_directory
import os

app = Flask(__name__)

# Use a very basic HTML template
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>DodanPyxel</title>
    <style>
        body {
            font-family: sans-serif;
            text-align: center;
            background-color: #121212;
            color: white;
            margin: 0;
            padding: 30px;
        }
        h1 {
            color: #66ccff;
        }
        .button {
            display: inline-block;
            background-color: #66ccff;
            color: black;
            padding: 12px 24px;
            text-decoration: none;
            margin: 10px;
            border-radius: 4px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>DodanPyxel - シューティングゲーム</h1>
    <p>縦スクロールシューティングゲーム - 10種類のボス、モバイル対応コントロール</p>
    
    <div>
        <a href="/download/windows" class="button">Windows版ダウンロード</a>
        <a href="/download/mac" class="button">macOS版ダウンロード</a>
        <a href="/download/source" class="button">ソースコードダウンロード</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/download/windows')
def download_windows():
    windows_zip = 'public/downloads/dodanpyxel-windows.zip'
    if not os.path.exists(windows_zip):
        if os.path.exists('web_static/downloads/dodanpyxel-windows.zip'):
            windows_zip = 'web_static/downloads/dodanpyxel-windows.zip'
    
    return send_file(windows_zip,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-windows.zip')

@app.route('/download/mac')
def download_mac():
    mac_zip = 'public/downloads/dodanpyxel-mac.zip'
    if not os.path.exists(mac_zip):
        if os.path.exists('web_static/downloads/dodanpyxel-mac.zip'):
            mac_zip = 'web_static/downloads/dodanpyxel-mac.zip'
    
    return send_file(mac_zip,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-mac.zip')

@app.route('/download/source')
def download_source():
    source_zip = 'public/downloads/dodanpyxel-source.zip'
    if not os.path.exists(source_zip):
        if os.path.exists('web_static/downloads/dodanpyxel-source.zip'):
            source_zip = 'web_static/downloads/dodanpyxel-source.zip'
    
    return send_file(source_zip,
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-source.zip')

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    print("Starting basic Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000)