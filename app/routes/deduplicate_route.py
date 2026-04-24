import json

from flask import request, render_template

from app.services.Mediator.mediator_delete import mediator_delete
from app.services.deduplicate_books import de_duplicate_books_refactor
from app.services.mediator import read


def deduplicate_route(main_app):
    @main_app.route('/book/deduplicate', methods=['POST', 'GET'])
    def dedup_page():
        user_settings_values = read({}, 'user-settings')

        if request.method == 'GET':
            response = de_duplicate_books_refactor()
            return render_template('deduplicate.html', book_result=response,
                                   user_settings=user_settings_values), 200
        else: #Implicit POST for Deleting a Book
            isbn = dict(request.form).get('ISBN')

            json_input = json.dumps({'ISBN': isbn})
            mediator_delete(json_input, 'dedupe')

            response = de_duplicate_books_refactor()
            return render_template('deduplicate.html', book_result=response,
                                   user_settings=user_settings_values), 200