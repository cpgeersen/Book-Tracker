from flask import request, render_template, jsonify, redirect, url_for, send_from_directory
from app.services.mediator import create, read, update, delete
#from app.services.openlibrary_api import search_books # temporary markout until added
from app.routes.test import test_bp
#from app.routes.pages import pages_bp
from app.services.create_db import create_db
import json
from app.services.create_example_records import create_sample_books
from app.services.create_many_records import create_many_records


SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500



# Create the Database
#create_db()
#create_sample_books()
#create_many_records(100)


def create_routes(app): # Placeholder returns for unfinished pages



    # Register Blueprints
    app.register_blueprint(test_bp)
    #app.register_blueprint(pages_bp)

    # Pages
    @app.route('/book/add-local', methods=['POST', 'GET'])
    def add_book_page():
        if request.method == 'POST':
            try:
                # First get the form information
                book_form_json = dict(request.form)

                # Next send to mediator for validation and creation
                book_response = create(book_form_json, 'book-local')

                # Read the result back to populate the individual page
                book_result = json.loads(read(book_form_json, 'book-isbn'))

                if book_response[1] == SUCCESS:
                    return redirect(url_for('individual_book_page', isbn=book_result['ISBN']))
                elif book_response[1] == FOUND:
                    return render_template('add_book.html'), FOUND # !WIP! add error page telling user book is already present
                elif book_response[1] == BAD_REQUEST:
                    return render_template('add_book.html'), BAD_REQUEST
            except TypeError as error:
                return render_template('add_book.html'), BAD_REQUEST # !WIP! add error page for malformed ISBN


        return render_template('add_book.html')

    @app.route('/book/isbn/<isbn>', methods=['GET', 'POST'])
    def individual_book_page(isbn):
        try:
            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}

            # Get the result in JSON format
            book_result = json.loads(read(isbn_dict, 'book-isbn'))

        # This error occurs when the ISBN does not exist in database
        except TypeError as error:
            return INTERNAL_SERVER_ERROR  # !WIP! add full error page

        if request.method == 'GET':
            # Display the result
            return render_template('view_book.html', book=book_result), 200

        elif request.method == 'POST':

            book_update = dict(request.form)
            print(book_update)

            if book_update.get('summary') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Summary': book_update['summary']})
                response = update(json_input, 'summary')

            elif book_update.get('chapters') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Chapters': book_update['chapters'],
                                         'Chapters_Completed': book_result['Chapters_Completed']})
                response = update(json_input, 'chapters')

            elif book_update.get('tag') is not None:
                json_input = json.dumps({'Tag_ID': book_result['Tag_ID'],
                                         'Owned': book_update['owned'],
                                         'Favorite': book_update['favorite'],
                                         'Completed': book_update['completed'],
                                         'Currently_Reading': book_update['currently_reading']})
                response = update(json_input, 'tag')

            elif book_update.get('chapters_completed') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Chapters_Completed': book_update['chapters_completed']})
                response = update(json_input, 'chapters-completed')
                print(response)

            elif book_update.get('delete') is not None:
                json_input = json.dumps({'ISBN': isbn})
                response = delete(json_input)

                return redirect('/book/local-search') # !!WIP!! give pop-up for success

            book_result = json.loads(read(isbn_dict, 'book-isbn'))
            return render_template('view_book.html', book=book_result), 200

        else:
            return render_template('view_book.html'), 200 # !!WIP!! Add Error for nonexistent book


    @app.route('/book/local-search', methods=['GET'])
    def local_search_page():
        search_type = request.args.get('search_type')

        if search_type == 'isbn':
            isbn = request.args.get('search', 'isbn')

            if len(isbn) == 0:
                book_result = read()
                return render_template('search.html', books=book_result, search_type='isbn'), 200

            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}
            try:
                book_result = json.loads(read(isbn_dict, 'book-isbn'))

                book_result = json.dumps({"Book_Result_1" : book_result})
                book_result = json.loads(book_result)

                if book_result == '':
                    return render_template('search.html', books={}, search_type='isbn'), 200

                return render_template('search.html', books=book_result, search_type='isbn'), 200
            except TypeError:   # When there is no book with ISBN match
                return render_template('search.html', books={}, search_type='isbn'), 200

        elif search_type == 'title':
            title = request.args.get('search', 'title')

            if len(title) == 0:
                book_result = read()
                return render_template('search.html', books=book_result, search_type='title'), 200

            title_json = {'Title': title.strip()}
            book_result = json.loads(read(title_json, 'book-title'))

            if dict(book_result).get('Error') == 'Title not found':
                return render_template('search.html', books={}, search_type='title'), 200
            else:
                return render_template('search.html', books=book_result, search_type='title'), 200

        elif search_type == 'author':
            author_name = request.args.get('search', 'author')
            author_name_list = author_name.split(' ')

            if len(author_name) == 0:
                book_result = read()
                return render_template('search.html', books=book_result, search_type='author'), 200

            match len(author_name_list):
                case 1:author_name_json = {'Author_Last_Name': author_name_list[0].strip().capitalize()}
                case 2: author_name_json = {'Author_Last_Name': author_name_list[1].strip().capitalize(),
                                            'Author_First_Name': author_name_list[0].strip().capitalize()}
                case _: return 'Not valid' # Add error pop up here

            book_result = json.loads(read(author_name_json, 'book-author'))

            if dict(book_result).get('Error') == 'Author not found':
                return render_template('search.html', books={}, search_type='author'), 200
            else:
                return render_template('search.html', books=book_result, search_type='author'), 200
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
    @app.route('/add-openlibrary', methods=['GET'])
    def add_openlibrary_page():
        return 'WIP', 200

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

if __name__ == '__main__':
    pass