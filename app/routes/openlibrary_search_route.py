from flask import request, render_template

from app.services.mediator import read, create

ol_search_page = 'ol_search/openlibrary_search.html'
ol_search_page_modal = 'ol_search/openlibrary_search_modal_isbn.html'


def openlibrary_search_route(main_app):
    @main_app.route('/add-openlibrary', methods=['POST', 'GET'])
    def openlibrary_search():
        if request.method == 'GET':
            search_type = request.args.get('search_type')

            if search_type == 'isbn':
                isbn = request.args.get('search', 'isbn')

                if len(isbn) == 0:
                    return render_template(ol_search_page), 200
                elif len(isbn) != 10 and len(isbn) != 13 or not str(isbn).isnumeric():
                    # Tell user that isbn must be either 10 or 13 integers
                    return render_template(ol_search_page_modal), 200

                isbn_dict = {"ISBN": isbn}
                response = read(isbn_dict, 'ol-book-isbn')

                return render_template(ol_search_page, books=response, search_type='isbn'), 200

            elif search_type == 'title':
                title = request.args.get('search', 'title')

                # If the search is empty or is too generic based on block_list, reload page
                block_list = ['the', 'a', 'be', 'that', 'of', 'this', 'and', 'by']
                if len(title) == 0 or title in block_list:
                    return render_template(ol_search_page), 200

                title_dict = {"Title": title}
                response = read(title_dict, 'ol-book-title')

                return render_template(ol_search_page, books=response, search_type='title'), 200

            elif search_type == 'author':
                author = request.args.get('search', 'author')

                # If the search is empty, reload page
                if len(author) == 0:
                    return render_template(ol_search_page), 200

                author_dict = {'Author_Name': author}
                response = read(author_dict, 'ol-book-author')

                return render_template(ol_search_page, books=response, search_type='author'), 200

            else:
                return render_template(ol_search_page), 200
        elif request.method == 'POST':
            # !! NOTICE !!
            # This is the only flask route method that uses fetch on the frontend
            # Fetch was required to prevent reload on book creation

            # Form received from a JS fetch request here
            add_book = dict(request.form)

            # Try and make a book here
            response = create(add_book, 'book-ol')

            # If the book is already present, send to the fetch request
            if response[1] == 302:
                return 'Error: Book all ready in database', 302

            # Otherwise the request was successful
            # It cannot be any other status codes since information being used
            # to create book is from the prevalidated cache
            return '', 204  # No Content (book present)

        else:
            # !!WIP!! Add error handling here
            return render_template(ol_search_page), 200