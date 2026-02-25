from flask import Blueprint,  request, render_template, jsonify

book_bp = Blueprint('book', __name__, url_prefix='/api/book/')

@book_bp.route('add', methods=['POST'])
def add_local_book(json1):
    if request.method == 'POST':
        book_form_json = request.form
        return f'<h1>{json1}</h1>'

    return render_template('add_book.html')
