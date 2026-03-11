from flask import request, render_template, jsonify, redirect, url_for
from app.services.mediator import create, read, update, delete
#from app.services.openlibrary_api import search_books # temporary markout until added
from app.routes.test import test_bp
from app.routes.pages import pages_bp
from app.services.create_db import create_db
import json


SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500



# Create the Database
#create_db()


def create_routes(app): # Placeholder returns for unfinished pages



    # Register Blueprints
    app.register_blueprint(test_bp)
    app.register_blueprint(pages_bp)

    # Pages
    @app.route('/book/add-local', methods=['POST', 'GET'])
    def add_book_page():
        if request.method == 'POST':
            # First get the form information
            book_form_json = dict(request.form)

            # Next send to mediator for validation and creation
            book_response = create(book_form_json, 'book-local')

            # Read the result back to populate the individual page
            book_result = json.loads(read(book_form_json, 'book-isbn'))

            if book_response[1] == SUCCESS:
                return redirect(url_for('individual_book_page', isbn=book_form_json['ISBN']))

            elif book_response[1] == BAD_REQUEST:
                return render_template('add_book.html')  # !WIP! add error page telling user book is already present

            else:
                return 'Server Error', 500

        return render_template('add_book.html')

    @app.route('/book/isbn/<isbn>')
    def individual_book_page(isbn):
        try:
            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}

            # Get the result in JSON format
            book_result = json.loads(read(isbn_dict, 'book-isbn'))

            # Display the result
            return render_template('view_book.html', book=book_result), 200

        # This error occurs when the ISBN does not exist in database
        except json.decoder.JSONDecodeError:
            return f'ISBN not in database'  # !WIP! add full error page

    @app.route('/book/local-search', methods=['GET'])
    def local_search_page():
        search_type = request.args.get('search_type')

        if search_type == 'isbn':
            isbn = request.args.get('search', 'isbn')

            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}
            try:
                book_result = json.loads(read(isbn_dict, 'book-isbn'))

                book_result = json.dumps({"Book_Result_1" : book_result})
                book_result = json.loads(book_result)

                if book_result == '':
                    return render_template('search.html', books={}), 200

                return render_template('search.html', books=book_result), 200
            except TypeError:   # When there is no book with ISBN match
                return render_template('search.html', books={}), 200

        elif search_type == 'title':
            pass
        elif search_type == 'author':
            pass
        else:
            try:
                book_result = read()
                return render_template('search.html', books=book_result), 200
            except TypeError: # When there are not books
                return render_template('search.html', books={}), 200



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



if __name__ == '__main__':
    pass