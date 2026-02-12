from flask import request

def create_routes(app):
    # Pages
    @app.route('/')
    def homepage():
        return 'Homepage', 200

    @app.route('/add-book')
    def add_book_page():
        return 'Add Books Here', 200

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
    #@app.route('/book/<int:isbn>/note')
    #def note_page(isbn):
    #    return f'Note for book with ISBN {isbn}'

    # Routes for POST, GET, UPDATE, DELETE
    # Book API Route
    @app.route('/book-api', methods=['POST', 'GET', 'UPDATE', 'DELETE'])
    def book_api():
        if request.method == 'POST':
            return 'POST'
        elif request.method == 'GET':
            return 'GET'
        elif request.method == 'UPDATE':
            return 'UPDATE'
        elif request.method == 'DELETE':
            return 'DELETE'
        return None # TEMP
