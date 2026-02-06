from flask import Flask
from app.test_route import create_flask_route


def create_app():
    # Creates the most basic Flask instance to test and a route
    app = Flask(__name__)
    create_flask_route(app)
    return app