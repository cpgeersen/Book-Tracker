import json

from flask import request, redirect, url_for, render_template

from app.services.mediator import create, read

# Status Codes
SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500


def add_local_book_route(main_app):
    @main_app.route('/book/add-local', methods=['POST', 'GET'])
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