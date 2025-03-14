from flask import Flask, send_file, render_template_string
import os
import sys

app = Flask(__name__)

# Extremely simple HTML template with all styling inlined
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>シューティングゲーム</title>
    <style>
        body {
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            background-color: #121212;
            color: #f0f0f0;
            text-align: center;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #66ccff;
            margin-bottom: 30px;
        }
        .download-btn {
            display: inline-block;
            background-color: #66ccff;
            color: #000;
            font-weight: bold;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 30px;
            font-size: 18px;
            margin: 20px;
        }
        .download-options {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            margin: 30px 0;
        }
        .download-box {
            flex-basis: 280px;
            margin: 10px;
            background-color: #1a1a1a;
            padding: 20px;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>DodanPyxel - 縦スクロールシューティングゲーム</h1>
        
        <div class="download-options">
            <div class="download-box">
                <h3>Windows版</h3>
                <p>Windows 10/11で動作します</p>
                <a href="/download/windows" class="download-btn">ダウンロード (.zip)</a>
            </div>
            
            <div class="download-box">
                <h3>macOS版</h3>
                <p>macOS 10.14以降で動作します</p>
                <a href="/download/mac" class="download-btn">ダウンロード (.zip)</a>
            </div>
            
            <div class="download-box">
                <h3>ソースコード</h3>
                <p>全プラットフォーム向け</p>
                <a href="/download/source" class="download-btn">ダウンロード (.zip)</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/download/windows')
def download_windows():
    # Create the ZIP file if it doesn't exist
    if not os.path.exists('web_static/downloads/dodanpyxel-windows.zip'):
        from create_windows_zip import create_windows_zip
        create_windows_zip()
    
    return send_file('web_static/downloads/dodanpyxel-windows.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-windows.zip')

@app.route('/download/mac')
def download_mac():
    # Create the ZIP file if it doesn't exist
    if not os.path.exists('web_static/downloads/dodanpyxel-mac.zip'):
        from create_mac_zip import create_mac_zip
        create_mac_zip()
    
    return send_file('web_static/downloads/dodanpyxel-mac.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-mac.zip')

@app.route('/download/source')
def download_source():
    # Create the ZIP file if it doesn't exist
    if not os.path.exists('web_static/downloads/dodanpyxel-source.zip'):
        from create_source_zip import create_source_zip
        create_source_zip()
    
    return send_file('web_static/downloads/dodanpyxel-source.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-source.zip')

@app.route('/health')
def health():
    return "OK"

if __name__ == '__main__':
    # Make sure the download directory exists
    os.makedirs('web_static/downloads', exist_ok=True)
    
    print("Starting ultra simple Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000)