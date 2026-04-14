import json

from flask import request, render_template

from app.services.genres import genres_for_table
from app.services.mediator import read


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


def local_search_route(main_app):
    @main_app.route('/book/local-search', methods=['GET'])
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
                # !!WIP!! may need a separate read since this uses other syntax, verify
                book_result = json.loads(read(isbn_dict, 'book-isbn-filtered', filter_json=filter_type))

                # When the book does not exist
                if book_result.get('Error') is not None or len(book_result) == 0:
                    book_result = ''
                else:
                    book_result = json.dumps({"Book_Result_1": book_result})
                    book_result = json.loads(book_result)

                if book_result == '':
                    return render_template('search.html', books={}, search_type='isbn',
                                           book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200

                return render_template('search.html', books=book_result, search_type='isbn',
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200
            except TypeError:  # When there is no book with ISBN match
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
                return render_template('search.html', books={}, search_type='title',
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
                case 1:
                    author_name_json = {'Author_Last_Name': author_name_list[0].strip()}
                case 2:
                    author_name_json = {'Author_Last_Name': author_name_list[1].strip(),
                                        'Author_First_Name': author_name_list[0].strip()}
                case _:
                    return 'Not valid'  # Add error pop up here

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
            except TypeError:  # When there are no books
                return render_template('search.html', books={},
                                       book_genres=BOOK_GENRES_SORTED, filter_json=filter_type), 200