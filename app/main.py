from flask import request, render_template, jsonify
from app.services.mediator import create, read, update, delete
from app.services.openlibrary_api import search_books

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
    #def openlibrary_search_page():
        #return 'OpenLibrary Search will be here', 200

    # this is all for testing purposes and will be changed to fit the frontend
    def openlibrary_search_page():
        # Read ?search=... from the URL
        query = request.args.get('search', '').strip()
        if not query:
            return jsonify(error='Missing query. Use /openlibrary-search?search=harry+potter'), 400

        # Call OpenLibrary service
        search_result = search_books(query)

        # If API/service fails, return upstream-style error
        if 'error' in search_result:
            return jsonify(search_result), 502

        # Keep only a few useful fields for the client
        docs = search_result.get('docs', [])
        trimmed_results = []
        for doc in docs[:5]:
            trimmed_results.append({
                'title': doc.get('title'),
                'author_name': doc.get('author_name', []),
                'first_publish_year': doc.get('first_publish_year'),
                'edition_count': doc.get('edition_count'),
            })

        # Return compact JSON payload
        return jsonify(query=query, num_found=search_result.get('numFound', 0), results=trimmed_results), 200

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
