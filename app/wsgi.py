# wsgi.py

from main import app

if __name__ == "__main__":
    from waitress import serve
    print("Starting production server with Waitress...")
    serve(app, host="0.0.0.0", port=5000)
