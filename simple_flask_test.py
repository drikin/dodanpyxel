from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Simple Flask Test</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1>Flask is working!</h1>
        <p>This is a simple test page for the Replit environment.</p>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    print("Starting simple Flask test on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)