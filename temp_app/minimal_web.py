from flask import Flask, send_from_directory

app = Flask(__name__)

# Serve static files from 'public' directory
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

# Add a specific health check endpoint
@app.route('/health')
def health():
    return 'OK'

if __name__ == '__main__':
    print("Starting minimal Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000)