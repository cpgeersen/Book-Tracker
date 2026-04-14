import json

from app.services.Book.Book import read_all_books, read_book, read_all_books_by_title, read_all_books_by_author, \
    read_book_notes
from app.services.Mediator.mediator_helpers import sort_results_by_title
from app.services.OpenLibrary.openlibrary import complete_book_from_isbn_ol, complete_books_from_title_ol, \
    complete_books_from_author_ol
from app.services.OpenLibrary.openlibrary_search_cache import cache
from app.services.filters.filter_search_results import filter_results, filter_results_isbn
from app.services.validate_json.validate_book_json import validate_book_for_frontend
from app.services.validate_json.validate_openlibrary_json import validate_isbn_search, validate_search_for_cache


def mediator_read(json_input, read_type, filter_json):
    try:
        if read_type == 'book-all':

            # Sort results ascending by title
            result = sort_results_by_title(read_all_books())

            if filter_json.get('filtered', 'false') == 'false':
                return result
            elif len(filter_json) != 0 or filter_json is not None:
                result = filter_results(filter_json, result)
                return result

        elif read_type == 'book-isbn':
            # First get the book record via ISBN
            result = read_book(json_input['ISBN'])
            # Then convert to frontend syntax for tags
            converted_result = validate_book_for_frontend(result)
            return converted_result

        elif read_type == 'book-isbn-filtered':
            # First get the book record via ISBN
            result = read_book(json_input['ISBN'])

            if filter_json.get('filtered', 'false') == 'false':
                return result
            elif len(filter_json) != 0 or filter_json is not None:
                result = json.loads(result)
                result = json.dumps(filter_results_isbn(filter_json, result))
                return result

        elif read_type == 'book-title':
            all_books_by_title = json.loads(read_all_books_by_title(json_input['Title']))

            if not isinstance(all_books_by_title, list):
                return json.dumps({"Error": "Title not found", "Status_Code": "404"})

            json_output = {}
            book_result_number = 1
            for book in all_books_by_title:
                json_output[f'Book_Result_{book_result_number}'] = book
                book_result_number += 1

            # Sort results ascending by title
            json_output = sort_results_by_title(json_output)

            if filter_json.get('filtered', 'false') == 'false':
                return json.dumps(json_output)
            elif len(filter_json) != 0 or filter_json is not None:
                result = json.dumps(filter_results(filter_json, json_output))
                return result

        elif read_type == 'book-author':
            all_books_by_author = json.loads(read_all_books_by_author(json_input['Author_Last_Name'],
                                                                      json_input.get('Author_First_Name')))

            if not isinstance(all_books_by_author, list):
                return json.dumps({"Error": "Author not found", "Status_Code": "404"})

            json_output = {}
            book_result_number = 1
            for book in all_books_by_author:
                # Accounts for a scenario where all author books are deleted
                # and the author is still in the database and can cause an empty
                # entry to show in the search frontend
                if book.get('Error') is not None:
                    continue
                json_output[f'Book_Result_{book_result_number}'] = book
                book_result_number += 1

            # Sort results ascending by title
            json_output = sort_results_by_title(json_output)

            if filter_json.get('filtered', 'false') == 'false':
                return json.dumps(json_output)
            elif len(filter_json) != 0 or filter_json is not None:
                result = json.dumps(filter_results(filter_json, json_output))
                return result

        elif read_type == 'note':
            response = read_book_notes(json_input)
            return response

        elif read_type == 'ol-book-isbn':
            isbn = json_input['ISBN']

            # First check if the search is in the cache
            cache_response = cache(isbn)

            if cache_response is None:
                print('Calling OpenLibrary API')

                # Pull OpenLibrary Data for ISBN
                ol_response = complete_book_from_isbn_ol(isbn)

                # Validate the data and put into an easier form
                validated_ol_response = validate_isbn_search(ol_response)

                # Add validated json to the cache
                cache_response = cache(isbn, validated_ol_response)

            cache_response.update({'ISBN': isbn})

            json_output = {'Book_Result_1': cache_response}

            return json_output

        elif read_type == 'ol-book-title':
            title = str(json_input['Title']).strip().lower()

            # First check if the search title is in the cache
            cache_response = cache(title)

            if cache_response is None:
                print('Calling OpenLibrary API')

                # Pull OpenLibrary data for title
                ol_response = complete_books_from_title_ol(title)

                # Validate the data and put into an easier form
                validated_ol_response = validate_search_for_cache(ol_response)

                # Add validated json to the cache
                cache_response = cache(title, validated_ol_response)

            return cache_response

        elif read_type == 'ol-book-author':
            author_name = str(json_input.get('Author_Name')).strip().lower()

            # Since we stripped the string, lacking a space means there is lack of either
            # first or last name
            if ' ' not in author_name:
                return {'Error': 'Author must have a first and last name.'}

            # Get the first and last portions of the author name
            author_first_name = author_name.split(' ')[0]
            author_last_name = author_name.split(' ')[-1]

            # First check if the search for author is in the cache
            cache_response = cache(author_name)

            if cache_response is None:
                print('Calling OpenLibrary API')

                # Pull OpenLibrary data for title
                ol_response = complete_books_from_author_ol(author_first_name, author_last_name)

                # Validate the data and put into an easier form
                validated_ol_response = validate_search_for_cache(ol_response)

                # Add validated json to the cache
                cache_response = cache(author_name, validated_ol_response)

            return cache_response




        else:
            return 'Error: Not a valid call'
    except:
        'TEMP EXCEPT'
