import json
import os
from pathlib import Path

from flask import request, render_template, redirect

from app.services.genres import genres_for_table
from app.services.mediator import read, update, delete, create

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


view_book_page = 'individual_book/view_book.html'
view_book_page_update_modal = 'individual_book/view_book_ol_update_modal.html'
search_page_modal = 'local_search/search_error_isbn.html'

def individual_book_route(main_app):
    # Small helper function for what files are allowed for cover images
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    UPLOAD_FOLDER = Path(main_app.static_folder) / "images" / "cover_images"

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @main_app.route('/book/isbn/<isbn>', methods=['GET', 'POST'])
    def individual_book_page(isbn):
        user_settings_values = read({}, 'user-settings')

        try:
            # Create a dict with the isbn, makes it possible to reuse mediator functions
            isbn_dict = {"ISBN": isbn}

            # When a book is locally created
            # Used to maintain context for redirect
            page = request.args.to_dict()

            # Get the result in JSON format
            book_result = json.loads(read(isbn_dict, 'book-isbn'))

            # Get notes if they exist
            note_result = read(isbn_dict, 'note')

        # This error occurs when the ISBN does not exist in database
        except TypeError as error:
            return render_template(search_page_modal, book_genres=BOOK_GENRES_SORTED,
                                   filter_json={}, user_settings=user_settings_values)

        if request.method == 'GET':
            # Display the result
            return render_template(view_book_page, book=book_result, notes=note_result,
                                   book_genres=BOOK_GENRES_SORTED, page_origin=page,
                                       user_settings=user_settings_values), 200

        elif request.method == 'POST':

            book_update = dict(request.form)

            if book_update.get('update_with_ol') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Update': book_update.get('update_cover'),
                                         'Summary_Update': book_update.get('update_summary')})
                response = update(json_input, 'openlibrary', main_app)

                book_result = json.loads(read(isbn_dict, 'book-isbn'))

                return render_template(view_book_page_update_modal, book=book_result, notes=note_result,
                                       book_genres=BOOK_GENRES_SORTED, updated_records=response, page_origin=page,
                                       user_settings=user_settings_values), 200

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
                                         'Currently_Reading': book_update['currently_reading'],
                                         'Personal_Or_Academic': book_update['personal_or_academic']})
                response = update(json_input, 'tag')

            elif book_update.get('chapters_completed') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Chapters_Completed': book_update['chapters_completed']})
                response = update(json_input, 'chapters-completed')

            elif book_update.get('delete') is not None:
                json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Path': book_result['Cover_Image']})
                response = delete(json_input, 'book')
                return redirect('/book/local-search')  # !!WIP!! give pop-up for success

            elif book_update.get('note-delete') is not None:
                json_input = json.dumps({'Note_ID': book_update['note_id']})
                response = delete(json_input, 'note')

            elif book_update.get('delete-genre') is not None:
                book_update.update({'ISBN': isbn})
                response = delete(book_update, 'genre')

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
                                         'Genre_1_Old': book_result['Genre_1'],
                                         'Genre_1_ID_Old': book_result['Genre_ID_1'],
                                         'Genre_2_Old': book_result.get('Genre_2'),
                                         'Genre_2_ID_Old': book_result.get('Genre_ID_2'),
                                         'Genre_3_Old': book_result.get('Genre_3'),
                                         'Genre_3_ID_Old': book_result.get('Genre_ID_3'),
                                         'Genre_4_Old': book_result.get('Genre_4'),
                                         'Genre_4_ID_Old': book_result.get('Genre_ID_4')
                                         })
                update(json_input, 'genres')


            elif book_update.get('cover-image') is not None:
                file = request.files['cover-image']

                # Gets the file extension for the image type
                file_extension = file.content_type.split('/')[-1]

                # Generates the file name and appends the file extension
                filename = isbn + '_' + 'cover_image' + '.' + file_extension

                file_path = os.path.join(main_app.config['UPLOAD_FOLDER'], Path(filename))

                if book_update.get('cover-image') == 'delete':
                    json_input = json.dumps({'ISBN': isbn, 'Cover_Image_Path': book_result['Cover_Image']})
                    response = delete(json_input, 'cover-image')
                    file.filename = ''

                # When a cover image is deleted or there was no cover image to begin with
                if file.filename == '':
                    book_result = json.loads(read(isbn_dict, 'book-isbn'))
                    note_result = read(isbn_dict, 'note')
                    return render_template(view_book_page, book=book_result,
                                           notes=note_result, book_genres=BOOK_GENRES_SORTED, page_origin=page,
                                           user_settings=user_settings_values), 200

                if file and allowed_file(file.filename):
                    # Saves the file to the images folder
                    file.save(file_path)
                    json_input = json.dumps(
                        {'ISBN': isbn, 'Cover_Image_Path': f'/static/images/cover_images/{filename}'})
                    response = update(json_input, 'cover-image')

            book_result = json.loads(read(isbn_dict, 'book-isbn'))
            note_result = read(isbn_dict, 'note')

            return render_template(view_book_page, book=book_result, notes=note_result,
                                   book_genres=BOOK_GENRES_SORTED, page_origin=page,
                                   user_settings=user_settings_values), 200

        else:
            return render_template(view_book_page, user_settings=user_settings_values), 200