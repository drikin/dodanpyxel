from flask import Flask, send_from_directory, render_template_string
import os
from create_windows_zip import create_windows_zip
from create_mac_zip import create_mac_zip
from create_source_zip import create_source_zip

app = Flask(__name__)

# Build game packages
def build_packages():
    # Ensure downloads directory exists
    if not os.path.exists('web_static/downloads'):
        os.makedirs('web_static/downloads', exist_ok=True)
    
    # Generate ZIP files
    create_windows_zip()
    create_mac_zip()
    create_source_zip()
    print("All game packages built successfully")

# Load HTML templates directly from files
def load_template(filename):
    with open(f"web_static/{filename}", "r") as f:
        return f.read()

# Main page
@app.route('/')
def index():
    return render_template_string(load_template("index.html"))

# Download page
@app.route('/download')
def download():
    return render_template_string(load_template("download.html"))

# Windows package
@app.route('/download/windows')
def download_windows():
    return send_from_directory('web_static/downloads', 'dodanpyxel-windows.zip')

# macOS package
@app.route('/download/mac')
def download_mac():
    return send_from_directory('web_static/downloads', 'dodanpyxel-mac.zip')

# Source code package
@app.route('/download/source')
def download_source():
    return send_from_directory('web_static/downloads', 'dodanpyxel-source.zip')

# Serve static images
@app.route('/screenshot.png')
def screenshot():
    return send_from_directory('web_static', 'screenshot.png')

if __name__ == '__main__':
    # First build packages
    build_packages()
    
    # Start server
    print("Starting server on port 5000...")
    app.run(host='0.0.0.0', port=5000)