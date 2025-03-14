from flask import Flask, render_template, send_file, redirect
import os
import sys
from create_windows_zip import create_windows_zip
from create_mac_zip import create_mac_zip
from create_source_zip import create_source_zip

app = Flask(__name__, static_folder='static')

# Ensure download directory exists
os.makedirs('static/downloads', exist_ok=True)

# Generate download packages if they don't exist
def ensure_downloads_exist():
    windows_zip = 'static/downloads/dodanpyxel-windows.zip'
    mac_zip = 'static/downloads/dodanpyxel-mac.zip'
    source_zip = 'static/downloads/dodanpyxel-source.zip'
    
    if not os.path.exists(windows_zip):
        print("Creating Windows package...")
        create_windows_zip()
        # Copy from web_static to static
        if os.path.exists('web_static/downloads/dodanpyxel-windows.zip'):
            os.system(f'cp web_static/downloads/dodanpyxel-windows.zip {windows_zip}')
    
    if not os.path.exists(mac_zip):
        print("Creating macOS package...")
        create_mac_zip()
        # Copy from web_static to static
        if os.path.exists('web_static/downloads/dodanpyxel-mac.zip'):
            os.system(f'cp web_static/downloads/dodanpyxel-mac.zip {mac_zip}')
    
    if not os.path.exists(source_zip):
        print("Creating source package...")
        create_source_zip()
        # Copy from web_static to static
        if os.path.exists('web_static/downloads/dodanpyxel-source.zip'):
            os.system(f'cp web_static/downloads/dodanpyxel-source.zip {source_zip}')

# Generate download packages when server starts
ensure_downloads_exist()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/download')
def download_page():
    return app.send_static_file('download.html')

@app.route('/screenshot.png')
def screenshot():
    return send_file('static/screenshot.png', mimetype='image/png')

@app.route('/download/windows')
def download_windows():
    return send_file('static/downloads/dodanpyxel-windows.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-windows.zip')

@app.route('/download/mac')
def download_mac():
    return send_file('static/downloads/dodanpyxel-mac.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-mac.zip')

@app.route('/download/source')
def download_source():
    return send_file('static/downloads/dodanpyxel-source.zip', 
                    mimetype='application/zip',
                    as_attachment=True,
                    download_name='dodanpyxel-source.zip')

if __name__ == '__main__':
    # Create directory for downloads
    os.makedirs('static/downloads', exist_ok=True)
    
    # Copy files from web_static if needed
    if not os.path.exists('static/screenshot.png') and os.path.exists('web_static/screenshot.png'):
        os.system('cp web_static/screenshot.png static/')
    
    # Copy HTML files to static folder
    if os.path.exists('index.html'):
        os.system('cp index.html static/')
    if os.path.exists('download.html'):
        os.system('cp download.html static/')
    
    # Copy downloads if they exist in web_static
    os.system('cp -r web_static/downloads/* static/downloads/ 2>/dev/null || true')
    
    print("Starting Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)