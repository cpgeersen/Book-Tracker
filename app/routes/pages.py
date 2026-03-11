from flask import Blueprint, render_template, request, jsonify
from app.services.mediator import create
from app.services.mediator import create, read
import json

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

# This route registers all the pages for the app

pages_bp = Blueprint('pages', __name__, url_prefix='/')

@pages_bp.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@pages_bp.route('/add-local', methods=['GET', 'POST'])
def add_book_page():
    if request.method == 'POST':
        # First get the form information
        book_form_json = dict(request.form)

        # Next send to mediator for validation and creation
        book_response = create(book_form_json, 'book-local')

        # Read the result back to populate the individual page
        book_result = json.loads(read(book_form_json, 'book-isbn'))

        if book_response[1] == SUCCESS:
            return render_template('view_book.html', book=book_result)

        elif book_response[1] == BAD_REQUEST:
            return render_template('add_book.html') # add error page telling user book is already present

        else:
            return 'Server Error', 500

    return render_template('add_book.html')

@pages_bp.route('/search', methods=['GET'])
def search_page():
    return render_template('search.html')

# WIP
@pages_bp.route('/add-openlibrary', methods=['GET'])
def add_openlibrary_page():
    return 'WIP', 200

# WIP
@pages_bp.route('/settings', methods=['GET'])
def settings_page():
    return 'WIP', 200

# WIP
@pages_bp.route('/dashboard', methods=['GET'])
def dashboard_page():
    return 'WIP', 200

# WIP (really only accessed through search page)
@pages_bp.route('/book/view', methods=['GET'])
def individual_book_page():
    book = []
    return render_template('view_book.html', book=book), 200

if __name__ == '__main__':
    pass