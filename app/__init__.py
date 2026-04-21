from app.test_route import create_test_flask_route
from app.main import create_routes

from flask import Flask, render_template, request


UPLOAD_FOLDER = './app/static/images/cover_images'

def create_app():
    app = Flask(__name__)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    create_routes(app)

    # 400 Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('search.html'), 400

    # 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('status_404.html'), 404

    # 500 Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('status_500.html'), 500

    return app