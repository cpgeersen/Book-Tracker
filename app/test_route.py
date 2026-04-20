from flask import Flask, jsonify
from app.test_route import create_test_flask_route
from app.main import create_routes

def create_test_flask_route(app):
    # Creates a basic test route that returns JSON with
    # a status of ok and 200
    @app.route('/test_route')
    def test_route():
        return jsonify(status='ok'), 200
