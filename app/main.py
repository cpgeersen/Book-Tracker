import os
import json
from pathlib import Path
from flask import request, render_template, jsonify, redirect, url_for, send_from_directory

from app.routes.add_local_book_route import add_local_book_route
from app.routes.individual_book_route import individual_book_route
from app.routes.local_search_route import local_search_route
from app.services.OpenLibrary.openlibrary_search_cache import create_cache
from app.services.mediator import create, read, update, delete
from app.routes.test import test_bp
from app.services.genres import genres_for_table
from app.services.mocking.create_example_records import create_sample_books
from app.services.mocking.create_many_records import create_many_records



# Status Codes
SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


# Book Genres for frontend
BOOK_GENRES = genres_for_table()
del BOOK_GENRES[1]
del BOOK_GENRES[2]
# Sorted by Alphabetic Order
BOOK_GENRES_SORTED = dict(sorted(BOOK_GENRES.items(), key=lambda kv: kv[1]))


# Small helper function for what files are allowed for cover images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = './app/static/images/cover_images'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Functions for mocking
#create_sample_books()
#create_many_records(100)

# Create OpenLibrary Search Cache
create_cache()

# Main Route Creation for the App
def create_routes(app):

    # Register Blueprints Used for Testing
    app.register_blueprint(test_bp)
    #app.register_blueprint(pages_bp)





    # Pages
    # Logic Found in Routes
    add_local_book_route(app)
    individual_book_route(app)
    local_search_route(app)


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
    @app.route('/add-openlibrary', methods=['POST', 'GET'])
    def openlibrary_search():
        if request.method == 'GET':
            search_type = request.args.get('search_type')

            if search_type == 'isbn':
                isbn = request.args.get('search', 'isbn')

                if len(isbn) == 0:
                    return render_template('openlibrary_search.html'), 200
                elif len(isbn) != 10 and len(isbn) != 13 or not str(isbn).isnumeric():
                    # Tell user that isbn must be either 10 or 13 integers
                    return render_template('openlibrary_search_modal_isbn.html'), 200


                isbn_dict = {"ISBN": isbn}
                response = read(isbn_dict, 'ol-book-isbn')

                return render_template('openlibrary_search.html', books=response,
                                       search_type='isbn'), 200

            elif search_type == 'title':
                title = request.args.get('search', 'title')

                # If the search is empty or is too generic based on block_list, reload page
                block_list = ['the', 'a', 'be', 'that', 'of', 'this', 'and', 'by']
                if len(title) == 0 or title in block_list:
                    return render_template('openlibrary_search.html'), 200

                title_dict = {"Title": title}
                response = read(title_dict, 'ol-book-title')

                return render_template('openlibrary_search.html', books=response,
                                       search_type='title'), 200

            elif search_type == 'author':
                author = request.args.get('search', 'author')

                # If the search is empty, reload page
                if len(author) == 0:
                    return render_template('openlibrary_search.html'), 200

                author_dict = {'Author_Name': author}
                response = read(author_dict, 'ol-book-author')

                return render_template('openlibrary_search.html', books=response,
                                       search_type='author'), 200

            else:
                return render_template('openlibrary_search.html'), 200
        elif request.method == 'POST':
            # !! NOTICE !!
            # This is the only flask route method that uses fetch on the frontend
            # Fetch was required to prevent reload on book creation

            # Form received from a JS fetch request here
            add_book = dict(request.form)

            # Try and make a book here
            response = create(add_book, 'book-ol')

            # If the book is already present, send to the fetch request
            if response[1] == 302:
                return 'Error: Book all ready in database', 302

            # Otherwise the request was successful
            # It cannot be any other status codes since information being used
            # to create book is from the prevalidated cache
            return '', 204 # No Content (book present)

        else:
            # !!WIP!! Add error handling here
            return render_template('openlibrary_search.html'), 200

    # WIP
    @app.route('/settings', methods=['GET'])
    def settings_page():
        return 'WIP', 200

    # WIP
    @app.route('/dashboard', methods=['GET'])
    def dashboard_page():
        return 'WIP', 200

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
