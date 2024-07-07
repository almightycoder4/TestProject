import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    if os.getenv("FLASK_ENV") == "production":
        from gunicorn.app.wsgiapp import WSGIApplication
        WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]").run()
    else:
        app.run(host='0.0.0.0', port=3100)
