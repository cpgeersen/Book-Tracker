import json

from flask import request, redirect, url_for, render_template

from app.services.mediator import create, read

# Status Codes
SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

'''
    Description: Creates the route for adding a book with local data. 
    Route listens are a POST or GET request from the frontend.
    
    Event:
        POST -> 
            Input: book_form_json (dict)
            Output: individual_book_page (route)
        GET -> 
            Output: add_book (html)
'''

def add_local_book_route(main_app):
    @main_app.route('/book/add-local', methods=['POST', 'GET'])
    def add_book_page():
        user_settings_values = read({}, 'user-settings')

        if request.method == 'POST':
            try:
                # First get the form information
                book_form_json = dict(request.form)

                # Next send to mediator for validation and creation
                book_response = create(book_form_json, 'book-local')

                # Read the result back to populate the individual page
                book_result = json.loads(read(book_form_json, 'book-isbn'))

                # Book is created without errors
                if book_response[1] == SUCCESS:
                    # Used to maintain context of route in redirect
                    page_origin = 'from_add_book'
                    return redirect(url_for('individual_book_page', isbn=book_result['ISBN'],  page_origin=page_origin,
                               user_settings=user_settings_values))

                elif book_response[1] == FOUND:
                    return render_template('add_book/add_book_error_present.html',
                               user_settings=user_settings_values)

                elif book_response[1] == BAD_REQUEST:
                    return render_template('add_book/add_book_error_malformed.html',
                               user_settings=user_settings_values), BAD_REQUEST

            except TypeError as error:
                return render_template('add_book/add_book_error_malformed.html',
                               user_settings=user_settings_values), BAD_REQUEST

        # Implicit GET request
        return render_template('add_book/add_book.html', user_settings=user_settings_values), SUCCESS