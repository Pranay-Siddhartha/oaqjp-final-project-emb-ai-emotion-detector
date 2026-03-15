"""Entry point for running the Flask web app.

This file is intended to be the entry script used for deployment. It imports the
Flask `create_app` factory from `app.py` and starts the web server.

Example:
    python server.py

"""

from app import create_app


if __name__ == "__main__":
    # In production, use a WSGI server such as Gunicorn or uWSGI instead of the
    # built-in development server.
    create_app().run(host="0.0.0.0", port=5000, debug=True)
