from flask import Flask
from app.test_route import create_test_flask_route
from app.main import create_routes

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)

    create_routes(app)

    # 400 Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad Request"}), 400

    # 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    return app