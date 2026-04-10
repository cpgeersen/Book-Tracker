import os
from pathlib import Path7
from fla00 sk import request, render_template, jsonify, redirect, url_for, send_from_directory
from app.services.mediator import create, read, update, delete
#from app.services.openlibrary_api import search_books # temporary markout until added
from app.routes.test import test_bp
import json
from app.services.genres import genres_for_table
from app.services.create_example_records import create_sample_books
from app.services.create_many_records import create_many_records
from app.services.openlibrary_search_cache import create_cache


SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = './app/static/images/cover_images'
BOOK_GENRES = genres_for_table()
del BOOK_GENRES[1]
del BOOK_GENRES[2]
BOOK_GENRES_SORTED = dict(sorted(BOOK_GENRES.items(), key=lambda kv: kv[1]))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create the Database
#create_db()
#create_sample_books()
#create_many_records(100)

# Create OpenLibrary Search Cache
create_cache()


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
                    return render_template('add_book_error_present.html'), FOUND
                elif book_response[1] == BAD_REQUEST:
                    return render_template('add_book_error_malformed.html'), BAD_REQUEST
            except TypeError as error:
                return render_template('add_book_error_malformed.html'), BAD_REQUEST


        return render_template('add_book.html')

    @app.route('/book/isbn/<isbn>', methods=['GET', 'POST'])
    def individual_book_page(isbn):
        try:
            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}

            # Get the result in JSON format
            book_result = json.loads(read(isbn_dict, 'book-isbn'))
            print(book_result)

            #Get notes if they exist
            note_result = read(isbn_dict, 'note')
            #print(note_result)

        # This error occurs when the ISBN does not exist in database
        except TypeError as error:
            return INTERNAL_SERVER_ERROR  # !WIP! add full error page

        if request.method == 'GET':
            # Display the result
            return render_template('view_book.html', book=book_result, notes=note_result,
                                   book_genres=BOOK_GENRES_SORTED), 200

        elif request.method == 'POST':

            book_update = dict(request.form)
            print(book_update)

            if book_update.get('update_with_ol') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Update': book_update.get('update_cover'),
                                         'Summary_Update': book_update.get('update_summary')})
                response = update(json_input, 'openlibrary')
                print(response)

                return render_template('view_book_ol_update_modal.html', book=book_result, notes=note_result,
                                       book_genres=BOOK_GENRES_SORTED, updated_records=response), 200

            elif book_update.get('summary') is not None:
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

            elif book_update.get('delete') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Path': book_result['Cover_Image']})
                response = delete(json_input, 'book')
                return redirect('/book/local-search') # !!WIP!! give pop-up for success

            elif book_update.get('note-delete') is not None:
                json_input = json.dumps({'Note_ID': book_update['note_id']})
                response = delete(json_input, 'note')

            elif book_update.get('note-edit') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Note_Content': book_update['note-edit'],
                                         'Note_ID': book_update['note_id']})
                response = create(json_input, 'note')

            elif book_update.get('update-genre') is not None:
                genre_1 = list(book_update['genre_1'].split(','))

                genre_2 = list(book_update['genre_2'].split(','))

                genre_3 = list(book_update['genre_3'].split(','))

                genre_4 = list(book_update['genre_4'].split(','))

                json_input = json.dumps({'ISBN': isbn,
                                         'Genre_1_New': genre_1[0].strip(), 'Genre_1_ID_New': genre_1[-1].strip(),
                                         'Genre_2_New': genre_2[0].strip(), 'Genre_2_ID_New': genre_2[-1].strip(),
                                         'Genre_3_New': genre_3[0].strip(), 'Genre_3_ID_New': genre_3[-1].strip(),
                                         'Genre_4_New': genre_4[0].strip(), 'Genre_4_ID_New': genre_4[-1].strip(),
                                         'Genre_1_Old': book_result['Genre_1'], 'Genre_1_ID_Old': book_result['Genre_ID_1'],
                                         'Genre_2_Old': book_result.get('Genre_2'), 'Genre_2_ID_Old': book_result.get('Genre_ID_2'),
                                         'Genre_3_Old': book_result.get('Genre_3'), 'Genre_3_ID_Old': book_result.get('Genre_ID_3'),
                                         'Genre_4_Old': book_result.get('Genre_4'), 'Genre_4_ID_Old': book_result.get('Genre_ID_4')
                                         })
                update(json_input, 'genres')


            elif book_update.get('cover-image') is not None:
                file = request.files['cover-image']

                # Gets the file extension for the image type
                file_extension = file.content_type.split('/')[-1]

                # Generates the file name and appends the file extension
                filename = isbn + '_' + 'cover_image' + '.' + file_extension

                file_path = os.path.join(app.config['UPLOAD_FOLDER'], Path(filename))

                if book_update.get('cover-image') == 'delete':
                    json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Path': book_result['Cover_Image']})
                    response = delete(json_input, 'cover-image')
                    file.filename = ''

                # When a cover image is deleted or there was no cover image to begin with
                if file.filename == '':
                    book_result = json.loads(read(isbn_dict, 'book-isbn'))
                    note_result = read(isbn_dict, 'note')
                    return render_template('view_book.html', book=book_result,
                                           notes=note_result, book_genres=BOOK_GENRES_SORTED), 200

                if file and allowed_file(file.filename):
                    # Saves the file to the images folder
                    file.save(file_path)
                    json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Path': f'/static/images/cover_images/{filename}'})
                    response = update(json_input, 'cover-image')


            book_result = json.loads(read(isbn_dict, 'book-isbn'))
            note_result = read(isbn_dict, 'note')

            return render_template('view_book.html', book=book_result, notes=note_result,
                                   book_genres=BOOK_GENRES_SORTED), 200

        else:
            return render_template('view_book.html'), 200


    @app.route('/book/local-search', methods=['GET'])
    def local_search_page():
        search_type = request.args.get('search_type')
        filter_type = dict(request.args)
        print(filter_type)

        if search_type == 'isbn':
            isbn = request.args.get('search', 'isbn')

            if len(isbn) == 0:
                book_result = read(filter_json=filter_type)

                return render_template('search.html', books=book_result, search_type='isbn',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}
            try:
                #!!WIP!! may need a separate read since this uses other syntax, verify
                book_result = json.loads(read(isbn_dict, 'book-isbn-filtered', filter_json=filter_type))

                # When the book does not exist
                if book_result.get('Error') is not None or len(book_result) == 0:
                    book_result = ''
                else:
                    book_result = json.dumps({"Book_Result_1" : book_result})
                    book_result = json.loads(book_result)

                if book_result == '':
                    return render_template('search.html', books={}, search_type='isbn',
                                           book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

                return render_template('search.html', books=book_result, search_type='isbn',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
            except TypeError:   # When there is no book with ISBN match
                return render_template('search.html', books={}, search_type='isbn',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

        elif search_type == 'title':
            title = request.args.get('search', 'title')

            if len(title) == 0:
                book_result = read(filter_json=filter_type)
                return render_template('search.html', books=book_result, search_type='title',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

            title_json = {'Title': title.strip()}
            book_result = json.loads(read(title_json, 'book-title', filter_json=filter_type))

            if dict(book_result).get('Error') == 'Title not found':
                return render_template('search.html', books={},search_type='title',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
            else:
                return render_template('search.html', books=book_result, search_type='title',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

        elif search_type == 'author':
            author_name = request.args.get('search', 'author')
            author_name_list = author_name.split(' ')

            if len(author_name) == 0:
                book_result = read(filter_json=filter_type)
                return render_template('search.html', books=book_result, search_type='author',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

            match len(author_name_list):
                case 1:author_name_json = {'Author_Last_Name': author_name_list[0].strip()}
                case 2: author_name_json = {'Author_Last_Name': author_name_list[1].strip(),
                                            'Author_First_Name': author_name_list[0].strip()}
                case _: return 'Not valid' # Add error pop up here

            book_result = json.loads(read(author_name_json, 'book-author', filter_json=filter_type))

            if dict(book_result).get('Error') == 'Author not found':
                return render_template('search.html', books={}, search_type='author',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
            else:
                return render_template('search.html', books=book_result, search_type='author',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
        else:
            try:
                book_result = read(filter_json=filter_type)
                return render_template('search.html', books=book_result,
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
            except TypeError: # When there are no books
                return render_template('search.html', books={},
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200



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
    @app.route('/add-openlibrary', methods=['POST', 'GET'])
    def openlibrary_search():
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
