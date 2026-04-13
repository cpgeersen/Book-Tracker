import json
import os
import requests

from app.services.Mediator.mediator_helpers import is_author_info_none, is_book_info_none, is_none
from app.services.genres import genres_for_table
from app.services.validate_book_json import validate_book_from_local, validate_book_for_frontend, validate_tags
from app.services.Book.Book import *
from app.services.filter_search_results import filter_results, filter_results_isbn
from app.services.openlibrary_api import search_books_by_title, get_work_data, search_books_by_isbn, \
    get_author_info_from_authorid, search_books_by_author, get_book_info_from_cover_key
from app.services.openlibrary_search_cache import cache
from app.services.validate_json.validate_openlibrary_json import validate_isbn_search, validate_search_for_cache

from app.services.openlibrary_data_resolution.resolve_author import resolve_author_olid

SUCCESS = 200
FOUND = 302
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500
BOOK_GENRES = genres_for_table()

def complete_book_from_isbn_ol(isbn):
    ol_data = search_books_by_isbn(isbn)

    if "error" in ol_data:
        return {"error": "ISBN not present in OpenLibrary, please use another ISBN or search via Title"}

    publish_year = ol_data.get("publish_date")

    publishers = ol_data.get("publishers", [])
    publisher = publishers[0] if publishers else None

    isbn_list = []
    if "isbn_10" in ol_data:
        isbn_list.extend(ol_data["isbn_10"])
    if "isbn_13" in ol_data:
        isbn_list.extend(ol_data["isbn_13"])

    cover_image_url = None
    if "covers" in ol_data and isinstance(ol_data["covers"], list) and len(ol_data["covers"]) > 0:
        cover_id = ol_data["covers"][0]
        cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

    work_key = None
    if "works" in ol_data and isinstance(ol_data["works"], list) and len(ol_data["works"]) > 0:
        if "key" in ol_data["works"][0]:
            work_key = ol_data["works"][0]["key"]

    author_1 = None
    author_1_olid = None
    author_2 = None
    author_2_olid = None
    publisher_olid = None
    summary = None
    title = None

    if work_key:
        work_data = get_work_data(work_key)

        if isinstance(work_data, dict):

            title = work_data.get("title")

            if "description" in work_data:
                if isinstance(work_data["description"], dict):
                    summary = work_data["description"].get("value")
                else:
                    summary = work_data["description"]

            if "publishers" in work_data:
                for pub in work_data["publishers"]:
                    if isinstance(pub, dict) and "key" in pub:
                        publisher_olid = pub["key"]
                        break

            if "authors" in work_data:
                authors = work_data["authors"]

                if len(authors) >= 1:
                    a1 = authors[0]
                    if "author" in a1 and "key" in a1["author"]:
                        author_1_olid = a1["author"]["key"]
                        a1_data = get_author_info_from_authorid(author_1_olid)
                        if isinstance(a1_data, dict):
                            author_1 = a1_data.get("name")

                if len(authors) >= 2:
                    a2 = authors[1]
                    if "author" in a2 and "key" in a2["author"]:
                        author_2_olid = a2["author"]["key"]
                        a2_data = get_author_info_from_authorid(author_2_olid)
                        if isinstance(a2_data, dict):
                            author_2 = a2_data.get("name")

    return {
        "Title": title,
        "Author_1": author_1,
        "Author_1_OLID": author_1_olid,
        "Author_2": author_2,
        "Author_2_OLID": author_2_olid,
        "Publisher": publisher,
        "Publisher_OLID": publisher_olid,
        "Summary": summary,
        "Publish_Year": publish_year,
        "Cover_Image_URL": cover_image_url
    }

def complete_books_from_title_ol(query, limit=5):
    search_results = search_books_by_title(query=query, limit=limit)

    if "error" in search_results:
        return search_results

    if "docs" not in search_results or len(search_results["docs"]) == 0:
        return {"error": "No search results found for the given title."}

    docs = search_results["docs"]
    final_results = {}

    for index, result in enumerate(docs, start=1):
        cover_edition_key = result.get('cover_edition_key')

        # When there is no cover edition key, iterate to the next
        # result since it is not usable without one
        if cover_edition_key is None:
            continue

        # Get book information about on result cover edition key
        cover_edition_result = get_book_info_from_cover_key(cover_edition_key)

        title = cover_edition_result.get("title")
        if title is None:
            continue

        # Not sure if we should have first year or publish year of this edition
        publish_year = result.get("first_publish_year")
        if publish_year is None:
            continue

        isbn = cover_edition_result.get('isbn_13')
        if isbn is not None:
            isbn = isbn[0]
        else:
            # Try to get an ISBN 10 number if ISBN 13 not available
            isbn = cover_edition_result.get('isbn_10')
            if isbn is not None:
                isbn = isbn[0]
            else:
                continue


        publisher = cover_edition_result.get('publishers')
        if publisher is not None:
            publisher = publisher[0]
        else:
            continue

        cover_image_url = None
        if "cover_i" in result:
            cover_id = result["cover_i"]
            cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        work_key = result.get("key")

        author_1 = None
        author_1_olid = None
        author_2 = None
        author_2_olid = None
        publisher_olid = None
        summary = None

        if work_key:
            work_data = get_work_data(work_key)

            if isinstance(work_data, dict):

                if "description" in work_data:
                    if isinstance(work_data["description"], dict):
                        summary = work_data["description"].get("value")
                    else:
                        summary = work_data["description"]

                if "publishers" in work_data:
                    for pub in work_data["publishers"]:
                        if isinstance(pub, dict) and "key" in pub:
                            publisher_olid = pub["key"]
                            break

                if "authors" in work_data:
                    authors = work_data["authors"]

                    if len(authors) >= 1:
                        a1 = authors[0]
                        if "author" in a1 and "key" in a1["author"]:
                            author_1_olid = a1["author"]["key"]
                            a1_data = get_author_info_from_authorid(author_1_olid)
                            if isinstance(a1_data, dict):
                                author_1 = a1_data.get("name")

                    if len(authors) >= 2:
                        a2 = authors[1]
                        if "author" in a2 and "key" in a2["author"]:
                            author_2_olid = a2["author"]["key"]
                            a2_data = get_author_info_from_authorid(author_2_olid)
                            if isinstance(a2_data, dict):
                                author_2 = a2_data.get("name")

        final_results[f"Book_Result_{index}"] = {
            "Title": title,
            "Publish_Year": publish_year,
            "ISBN": isbn,
            "Publisher": publisher,
            "Publisher_OLID": publisher_olid,
            "Author_1": author_1,
            "Author_1_OLID": author_1_olid,
            "Author_2": author_2,
            "Author_2_OLID": author_2_olid,
            "Summary": summary,
            "Cover_Image_URL": cover_image_url
        }

    return final_results

def complete_books_from_author_ol(first_name, last_name, limit=5):
    search_results = search_books_by_author(first_name, last_name, limit=limit)

    if "error" in search_results:
        return search_results

    if "docs" not in search_results or len(search_results["docs"]) == 0:
        return {"error": "No search results found for the given author."}

    docs = search_results["docs"]
    final_results = {}

    for index, result in enumerate(docs, start=1):
        cover_edition_key = result.get('cover_edition_key')

        # When there is no cover edition key, iterate to the next
        # result since it is not usable without one
        if cover_edition_key is None:
            continue

        # Get book information about on result cover edition key
        cover_edition_result = get_book_info_from_cover_key(cover_edition_key)

        title = cover_edition_result.get("title")
        if title is None:
            continue

        # Not sure if we should have first year or publish year of this edition
        publish_year = result.get("first_publish_year")
        if publish_year is None:
            continue

        isbn = cover_edition_result.get('isbn_13')
        if isbn is not None:
            isbn = isbn[0]
        else:
            # Try to get an ISBN 10 number if ISBN 13 not available
            isbn = cover_edition_result.get('isbn_10')
            if isbn is not None:
                isbn = isbn[0]
            else:
                continue


        publisher = cover_edition_result.get('publishers')
        if publisher is not None:
            publisher = publisher[0]
        else:
            continue

        cover_image_url = None
        if "cover_i" in result:
            cover_id = result["cover_i"]
            cover_image_url = f"https://covers.openlibrary.org/b/id/{cover_id}-L.jpg"

        work_key = result.get("key")

        author_1 = None
        author_1_olid = None
        author_2 = None
        author_2_olid = None
        publisher_olid = None
        summary = None

        if work_key:
            work_data = get_work_data(work_key)

            if isinstance(work_data, dict):

                if "description" in work_data:
                    if isinstance(work_data["description"], dict):
                        summary = work_data["description"].get("value")
                    else:
                        summary = work_data["description"]

                if "publishers" in work_data:
                    for pub in work_data["publishers"]:
                        if isinstance(pub, dict) and "key" in pub:
                            publisher_olid = pub["key"]
                            break

                if "authors" in work_data:
                    authors = work_data["authors"]

                    if len(authors) >= 1:
                        a1 = authors[0]
                        if "author" in a1 and "key" in a1["author"]:
                            author_1_olid = a1["author"]["key"]
                            a1_data = get_author_info_from_authorid(author_1_olid)
                            if isinstance(a1_data, dict):
                                author_1 = a1_data.get("name")

                    if len(authors) >= 2:
                        a2 = authors[1]
                        if "author" in a2 and "key" in a2["author"]:
                            author_2_olid = a2["author"]["key"]
                            a2_data = get_author_info_from_authorid(author_2_olid)
                            if isinstance(a2_data, dict):
                                author_2 = a2_data.get("name")

        final_results[f"Book_Result_{index}"] = {
            "Title": title,
            "Publish_Year": publish_year,
            "ISBN": isbn,
            "Publisher": publisher,
            "Publisher_OLID": publisher_olid,
            "Author_1": author_1,
            "Author_1_OLID": author_1_olid,
            "Author_2": author_2,
            "Author_2_OLID": author_2_olid,
            "Summary": summary,
            "Cover_Image_URL": cover_image_url
        }

    return final_results
# POST - Takes JSON as input
def create(json_input, create_type):
    try:
        if create_type == 'book-local':
            isbn = json_input['ISBN']

            # !!WIP!! Note: This fix my break, look out in future
            if not is_in_book_table(isbn):
                json.dumps({'Error': 'Book already in database'}), FOUND
            json_input = validate_book_from_local(json_input)
            result = create_book(json_input)
            return result

        elif create_type == 'book-ol':
            isbn = json_input['ISBN']

            if not is_in_book_table(isbn):
                json.dumps({'Error': 'Book already in database'}), FOUND

            # Get URL before validating json
            image_url = json_input['Cover_Image_URL']

            json_input = validate_book_from_local(json_input)

            result = create_book(json_input)

            # When the book exists, do not create the cover image again
            if result[1] == 302:
                return result

            # Download cover image from cache_response['Cover_Image_URL']
            # to /static/cover_images
            image_data = requests.get(image_url).content

            # Use cover image naming, uses jpg since OL stores cover images this way
            file_name = isbn + '_' + 'cover_image.jpg'
            file_path = os.path.join('app', 'static', 'images', 'cover_images', file_name)

            # Write the images to the correct path
            with open(file_path, 'wb') as image:
                image.write(image_data)

            # Update cover image file path in database
            update_book_cover_image(isbn, f'/static/images/cover_images/{file_name}')

            return result
            # !!WIP!! Error here
            return 'WIP'

        elif create_type == 'note':
            json_input = json.loads(json_input)
            if len(json_input.get('Note_Content')) > 0:
                note_id_in_database = is_note_id_in_database(json_input)
                if not note_id_in_database:
                    result = create_book_note(json_input)
                    return result
                else:
                    result = update_book_note(json_input)
                    return result
            else:
                return json.dumps({'Error': 'Empty Note'})
        else:
            return 'Error: Not a valid call'
    except (TypeError, ValueError, AttributeError):
        return f'Error: Invalid Entry, could not parse. Try again.', BAD_REQUEST
    except KeyError as error: # If any required keys are missing from JSON
        return error, BAD_REQUEST

# GET - Takes JSON as input
def read(json_input=None, read_type='book-all', filter_json=None):
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

            return  json_output

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




# PATCH - Takes JSON as input
def update(json_input, update_type):
    try:
        if update_type == 'summary':
            json_input = json.loads(json_input)
            response = update_book_summary(json_input['ISBN'], json_input['Summary'])
            return response

        elif update_type == 'chapters':
            json_input = json.loads(json_input)
            if json_input['Chapters_Completed'] > json_input['Chapters']:
                update_book_chapters_completed(json_input['ISBN'], json_input['Chapters'])

            response = update_book_chapters(json_input['ISBN'], json_input['Chapters'])
            return response

        elif update_type == 'chapters-completed':
            json_input = json.loads(json_input)
            response = update_book_chapters_completed(json_input['ISBN'], json_input['Chapters_Completed'])
            return response

        elif update_type == 'tag':
            json_input = json.loads(json_input)
            json_input_converted_tags = validate_tags(json_input)
            response = update_book_tags(json_input['Tag_ID'], json_input_converted_tags['Owned'],
                                        json_input_converted_tags['Favorite'], json_input_converted_tags['Completed'],
                                        json_input_converted_tags['Currently_Reading'])
            return response

        elif update_type == 'cover-image':
            json_input = json.loads(json_input)
            response = update_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
            return response

        elif update_type == 'genres':
            json_input = dict(json.loads(json_input))

            genre_number = 1
            while genre_number < 5:
                print(type(json_input[f'Genre_{genre_number}_ID_Old']))
                if json_input[f'Genre_{genre_number}_ID_Old'] is None:
                    print('here')
                    if json_input[f'Genre_{genre_number}_ID_New'] == 'None':
                        print('continue')
                        genre_number += 1
                        continue
                    else:
                        print('create')
                        create_book_genre(json_input['ISBN'], json_input[f'Genre_{genre_number}_ID_New'])


                if json_input[f'Genre_{genre_number}_ID_New'] != json_input[f'Genre_{genre_number}_ID_Old']:
                    update_book_genre(json_input['ISBN'], json_input[f'Genre_{genre_number}_ID_Old'],
                                      json_input[f'Genre_{genre_number}_ID_New'])

                genre_number += 1

        elif update_type == 'openlibrary':
            json_input = json.loads(json_input)
            isbn = json_input['ISBN']

            # Get current book information
            old_json_data = json.loads(read_book(isbn))

            # First see if book information is in cache
            cache_response = cache(isbn)

            #Creates a new cache record when none exist
            if cache_response is None:
                print('Calling OpenLibrary API')

                # Pull OpenLibrary Data for ISBN
                ol_response = complete_book_from_isbn_ol(isbn)

                # Validate the data and put into an easier form
                validated_ol_response = validate_isbn_search(ol_response, isbn)

                # Add validated json to the cache
                cache_response = cache(isbn, validated_ol_response)

            is_cover_image_updated = False
            if json_input.get('Cover_Image_Update') is not None:
                # Download cover image from cache_response['Cover_Image_URL']
                # to /static/cover_images
                image_url = cache_response['Cover_Image_URL']
                image_data = requests.get(image_url).content

                # Use cover image naming, uses jpg since OL stores cover images this way
                file_name = isbn + '_' + 'cover_image.jpg'
                file_path = os.path.join('app', 'static', 'images', 'cover_images', file_name)

                # Write the images to the correct path
                with open(file_path, 'wb') as image:
                    image.write(image_data)

                # Update cover image file path in database
                update_book_cover_image(isbn, f'/static/images/cover_images/{file_name}')
                is_cover_image_updated = True

            # Update book title if not correct
            old_title = old_json_data.get('Title')
            cache_title = cache_response.get('Title')
            is_title_update = False

            if not is_book_info_none(cache_title, old_title):
                update_book_title(isbn, cache_title)
                is_title_update = True

            # Update book summary if requested
            old_summary = old_json_data.get('Summary')
            cache_summary = cache_response.get('Summary')
            is_summary_updated = False

            if not is_book_info_none(old_summary, cache_summary):
                update_book_summary(isbn, cache_summary)
                is_summary_updated = True

            # Update author names
            cache_author_1_olid = cache_response.get('Author_1_OLID')
            is_author_1_updated = False

            if not is_author_info_none(cache_author_1_olid):
                is_author_1_updated = resolve_author_olid(old_json_data, cache_response, author_num='1')

            # When there is a second author
            cache_author_2_olid = cache_response.get('Author_2_OLID')
            is_author_2_updated = False

            if not is_author_info_none(cache_author_2_olid):
                is_author_2_updated = resolve_author_olid(old_json_data, cache_response, author_num='2')

            # There is a second author, but there should not be one
            elif not is_none(old_json_data.get('Author_First_Name_2')):
                delete_book_author_record(old_json_data.get('ISBN'),
                                          old_json_data.get('Author_First_Name_2'),
                                          old_json_data.get('Author_Last_Name_2'))

            # Update book publish year if possible
            old_publisher_year = old_json_data.get('Publish_Year')
            cache_publish_year = cache_response.get('Publish_Year')
            is_publish_year_updated = False

            if not is_book_info_none(cache_publish_year, old_publisher_year):
                update_book_publisher_year(isbn, cache_publish_year)
                is_publish_year_updated = True

            # Update publisher information
            cache_publisher_name = cache_response.get('Publisher_Name')
            old_publisher_name = old_json_data.get('Publisher_Name')
            is_publisher_updated = False

            if not is_book_info_none(cache_publisher_name, old_publisher_name):
                # Check if the new publisher already in the database
                is_publisher_present = is_publisher_in_database(cache_publisher_name)

                if is_publisher_present:
                    publisher_id = read_publisher_id_by_name(cache_publisher_name)['Publisher_ID']
                    update_book_publisher_id(old_json_data.get('ISBN'), publisher_id[0])
                    is_publisher_updated = True
                else:
                    # Publisher is not present, create new publisher with data and update
                    publisher_id = create_new_publisher(cache_publisher_name)['Publisher_ID']
                    update_book_publisher_id(old_json_data.get('ISBN'), publisher_id[0])
                    is_publisher_updated = True

            # Builds dict for updated items
            updated_records = {'Updated': 'False'}
            if is_title_update:
                updated_records['Title'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_summary_updated:
                updated_records['Summary'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_publish_year_updated:
                updated_records['Publish_Year'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_cover_image_updated:
                updated_records['Cover_Image'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_publisher_updated:
                updated_records['Publisher'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_author_1_updated:
                updated_records['Author_1'] = 'Updated'
                updated_records['Updated'] = 'True'

            if is_author_2_updated:
                updated_records['Author_2'] = 'Updated'
                updated_records['Updated'] = 'True'

            return updated_records




            # Call author case and publisher case function here

    except TypeError:
        pass    # !!WIP TypeError!!


# DELETE - Takes JSON as input
def delete(json_input, delete_type):
    if delete_type == 'book':
        json_input = json.loads(json_input)
        delete_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
        delete_book(json_input['ISBN'])

        note_ids = read_book_notes(json_input)
        for value in note_ids.values():
            rep = delete_book_note(value)

        return json.dumps({'Success': 'Book Deleted'})

    elif delete_type == 'note':
        json_input = json.loads(json_input)
        response = delete_book_note(json_input)
        return response

    elif delete_type == 'cover-image':
        json_input = json.loads(json_input)
        response = delete_book_cover_image(json_input['ISBN'], json_input['Cover_Image_Path'])
        return response

    else:
        return 'Error: Not a valid call'


def sort_results_by_title(result):
    result = dict(sorted(result.items(), key=lambda kv: kv[1]['Title']))
    return result



if __name__ == '__main__':
    #main()
    pass