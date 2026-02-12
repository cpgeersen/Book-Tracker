from flask import request, jsonify, render_template
from app.mediator import create, read, update, delete

json = {'test': 'value'}


def create_routes(app): # Placeholder returns for unfinished pages
    # Pages
    @app.route('/')
    def homepage():
        return 'Homepage', 200

    @app.route('/add-book')
    def add_book_page():
        return render_template('add_book.html')

    @app.route('/local-search')
    def local_search_page():
        return 'Search Local Database Here', 200

    @app.route('/openlibrary-search')
    def openlibrary_search_page():
        return 'OpenLibrary Search will be here', 200

    @app.route('/book/')
    def individual_book_pages():
        return 'Individual Book Pages will be here', 200

    # WIP
    # @app.route('/book/<int:isbn>/note')
    # def note_page(isbn):
    #    return f'Note for book with ISBN {isbn}'

    # Routes for POST, GET, UPDATE, DELETE
    # Book API Route
    @app.route('/book-api', methods=['POST', 'GET', 'PATCH', 'DELETE'])
    def book_api():
        if request.method == 'POST':
            return create(json)
        elif request.method == 'GET':
            return read(json)
        elif request.method == 'PATCH':
            return update(json)
        elif request.method == 'DELETE':
            return delete(json)
        return None  # TEMP
