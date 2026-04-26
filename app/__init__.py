from pathlib import Path

from flask import Flask, render_template, request

from app.main import create_routes
from app.test_route import create_test_flask_route


def create_app():
    app = Flask(__name__)

    upload_folder = Path(app.static_folder) / "images" / "cover_images"
    upload_folder.mkdir(parents=True, exist_ok=True)

    app.config["UPLOAD_FOLDER"] = str(upload_folder)

    create_routes(app)

    # 400 Bad Request
    @app.errorhandler(400)
    def bad_request(error):
        return render_template('search.html'), 400

    # 404 Not Found
    @app.errorhandler(404)
    def not_found(error):
        return render_template('error_pages/status_404.html'), 404

    # 500 Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('error_pages/status_500.html'), 500

    return app