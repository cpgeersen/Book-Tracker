from flask import Blueprint, render_template, request, jsonify
from app.services.mediator import create
from app.services.create_complete_book import create_book_record
from app.services.full_read_book import read_full_book_record


# This route registers all the pages for the app

pages_bp = Blueprint('pages', __name__, url_prefix='/')

@pages_bp.route('/', methods=['GET'])
def homepage():
    return render_template('homepage.html')

@pages_bp.route('/add-local', methods=['GET', 'POST'])
def add_book_page():
    if request.method == 'POST':
        print('test')
        book_form_json = dict(request.form)
        #print(book_form_json)
        book_response = create_book_record(book_form_json)
        print(book_response)
        print(read_full_book_record(book_form_json['ISBN']))

        #create(book_form_json, 'book')
        #print(book_form_json)

        return render_template('add_book.html')
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
    return render_template('view_book.html'), 200
