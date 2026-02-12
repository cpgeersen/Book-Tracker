from flask import Flask
from app.test_route import create_test_flask_route
from app.main import create_routes

DEBUG = True # Make False for release

if DEBUG:
    def create_app():
        # Creates the most basic Flask instance to test and a route
        app = Flask(__name__)  # Warning is fine for this usage
        create_test_flask_route(app)
        create_routes(app)
        return app
else:  # Start app without testing enabled
    app = Flask(__name__)
    create_routes(app)
