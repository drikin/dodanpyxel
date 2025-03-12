from flask import Flask, send_from_directory
import os
from create_windows_zip import create_windows_zip
from create_mac_zip import create_mac_zip
from create_source_zip import create_source_zip

app = Flask(__name__, static_folder='web_static')

# Build game packages
def build_game_packages():
    # Ensure downloads directory exists
    if not os.path.exists('web_static/downloads'):
        os.makedirs('web_static/downloads', exist_ok=True)
    
    # Generate ZIP files
    create_windows_zip()
    create_mac_zip()
    create_source_zip()
    print("All game packages built successfully")

# Home page
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Download page
@app.route('/download')
def download():
    return app.send_static_file('download.html')

# Download Windows package
@app.route('/downloads/dodanpyxel-windows.zip')
def download_windows():
    return send_from_directory('web_static/downloads', 'dodanpyxel-windows.zip')

# Download macOS package
@app.route('/downloads/dodanpyxel-mac.zip')
def download_mac():
    return send_from_directory('web_static/downloads', 'dodanpyxel-mac.zip')

# Download source package
@app.route('/downloads/dodanpyxel-source.zip')
def download_source():
    return send_from_directory('web_static/downloads', 'dodanpyxel-source.zip')

# Static file handler
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    # Build packages before starting server
    build_game_packages()
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False)