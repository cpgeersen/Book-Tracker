from flask import render_template, send_from_directory

# Route imports
from app.routes.add_local_book_route import add_local_book_route
from app.routes.individual_book_route import individual_book_route
from app.routes.local_search_route import local_search_route
from app.routes.openlibrary_search_route import openlibrary_search_route
from app.services.OpenLibrary.openlibrary_search_cache import create_cache
from app.services.deduplicate_books import de_duplicate_books, de_duplicate_books_refactor

# Test Route Import
from app.routes.test import test_bp

# Imports used for Mocking
from app.services.mocking.create_example_records import create_sample_books
from app.services.mocking.create_many_records import create_many_records


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


    @app.route('/', methods=['GET'])
    def homepage():
        return render_template('homepage.html')

    @app.route('/template-assets/<path:filename>', methods=['GET'])
    def template_asset(filename):
        return send_from_directory(app.template_folder, filename)

    @app.route('/search', methods=['GET'])
    def search_page():
        return render_template('search.html')

    # WIP
    @app.route('/settings', methods=['GET'])
    def settings_page():
        return 'WIP', 200

    # WIP
    @app.route('/book/deduplicate', methods=['POST', 'GET'])
    def dedup_page():
        response = de_duplicate_books_refactor()
        #print(response)
        return render_template('deduplicate.html', book_result=response), 200

#------------------------------------------------------
# Author: Christopher O'Brien
# 03.30.26
# [Y/N] APPROVED (username)
# Description: This function works to populate the Jinja User Profile template
#------------------------------------------------------
    @app.route("/analytics")
    def analytics():
        return 'WIP', 200
    #import Analytic_FunctionRefactored as AF

    #@app.route("/analytics")
    #def analytics():
    #    cursor = get_db_cursor()  # however you obtain it

    #    data = {
    #        "favorite_genre": AF.get_favorite_genre(cursor),
    #        "total_books": AF.get_total_books(cursor),
    #        "owned_books": AF.get_owned_books(cursor),
    #        "currently_reading": AF.get_currently_reading(cursor),
    #        "completed": AF.get_completed(cursor)
    #    }

    #return render_template("analytics.html", **data)

if __name__ == '__main__':
    pass
