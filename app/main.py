from flask import request, render_template
from app.services.mediator import create, read, update, delete

json = {'author': 'John Doe',
        'author2': '',
        'chapters': 30,
        'fiction-or-nonfiction': 'fiction',
        'isbn': 1234567890123,
        'owned': 'on',
        'personal-or-academic': 'personal',
        'publisher': 'SomePublisher',
        'title': 'BookTitle',
        'year-published': '2026',}


def create_routes(app): # Placeholder returns for unfinished pages
    # Pages
    @app.route('/')
    def homepage():
        return 'Homepage', 200

    @app.route('/add-book', methods=['POST', 'GET'])
    def add_book_page():
        if request.method == 'POST':
            #create_book_json = dict(request.form) # Pulls from the actual frontend
            create_book_json = dict(json) # Testing values
            return create(create_book_json,"book") # Will add new template denoting success and will link to new book
        return render_template('test_add_book.html')

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
