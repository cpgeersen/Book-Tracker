import json
import os

from flask import render_template, request

# Route imports
from app.routes.add_local_book_route import add_local_book_route
from app.routes.dashboard import dashboard_route
from app.routes.individual_book_route import individual_book_route
from app.routes.local_search_route import local_search_route
from app.routes.openlibrary_search_route import openlibrary_search_route
from app.routes.settings_route import settings_route
from app.services.Mediator.mediator_delete import mediator_delete
from app.services.OpenLibrary.openlibrary_search_cache import create_cache
from app.services.deduplicate_books import de_duplicate_books_refactor

# Test Route Import
from app.routes.test import test_bp
from app.services.mediator import read

# Imports used for Mocking
from app.services.mocking.create_example_records import create_sample_books
from app.services.mocking.create_many_records import create_many_records
from app.services.user_settings.user_settings import create_user_settings_json

# Status Codes
SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


# Functions for mocking
#create_sample_books()
#create_many_records(100)

# Create OpenLibrary Search Cache
create_cache()

# Create User Settings
create_user_settings_json()

# Creates the Cover Image Path
cover_image_path = os.path.join("app", "static", "images", "cover_images")
try:
    os.mkdir(cover_image_path)
except FileExistsError:
    pass    # passively ignore if the directory exists


# Main Route Creation for the App
def create_routes(app):

    # Register Blueprints Used for Testing
    app.register_blueprint(test_bp)

    # Pages
    # Logic Found in Routes
    # ./app/routes
    add_local_book_route(app)
    individual_book_route(app)
    local_search_route(app)
    openlibrary_search_route(app)
    settings_route(app)
    dashboard_route(app)


    @app.route('/', methods=['GET'])
    def homepage():
        user_settings_values = read({}, 'user-settings')
        return render_template('homepage.html', user_settings=user_settings_values)

    @app.route('/book/deduplicate', methods=['POST', 'GET'])
    def dedup_page():
        if request.method == 'GET':
            response = de_duplicate_books_refactor()
            return render_template('deduplicate.html', book_result=response), 200
        else: #Implicit POST for Deleting a Book
            isbn = dict(request.form).get('ISBN')

            json_input = json.dumps({'ISBN': isbn})
            mediator_delete(json_input, 'dedupe')

            response = de_duplicate_books_refactor()
            return render_template('deduplicate.html', book_result=response), 200


if __name__ == '__main__':
    pass
