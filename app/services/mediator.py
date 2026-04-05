import json

import requests
from app.services.genres import genres_for_table
from app.services.validate_book_json import validate_book_from_local, validate_book_for_frontend, validate_tags
from app.services.Book.Book import (create_book, read_book, read_all_books, read_all_books_by_title,
                                    read_all_books_by_author, update_book_summary, update_book_chapters,
                                    update_book_chapters_completed, update_book_tags, delete_book,
                                    create_book_note, read_book_notes, update_book_note, update_book_cover_image,
                                    delete_book_note, is_note_id_in_database, update_book_genre, create_book_genre,
                                    delete_book_cover_image, is_in_book_table)
from app.services.filter_search_results import filter_results, filter_results_isbn
from app.services.openlibrary_api import search_books_by_title, get_work_data, search_books_by_isbn, \
    get_author_info_from_authorid, search_books_by_author

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

    return {
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
        title = result.get("title")
        publish_year = result.get("first_publish_year")

        isbn_list = result.get("isbn", [])
        isbn = isbn_list[0] if isbn_list else None

        publishers = result.get("publisher", [])
        publisher = publishers[0] if publishers else None

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
        title = result.get("title")
        publish_year = result.get("first_publish_year")

        isbn_list = result.get("isbn", [])
        isbn = isbn_list[0] if isbn_list else None

        publishers = result.get("publisher", [])
        publisher = publishers[0] if publishers else None

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
            # !!WIP!! Note: This fix my break, look out in future
            if not is_in_book_table(json_input['ISBN']):
                json.dumps({'Error': 'Book already in database'}), FOUND
            json_input = validate_book_from_local(json_input)
            result = create_book(json_input)
            return result

        elif create_type == 'book-ol':
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

        elif create_type == 'cover-image':
            return 'WIP'
        else:
            return 'Error: Not a valid call'
    except TypeError, ValueError, AttributeError:
        return f'Error: Invalid Entry, could not parse. Try again.', BAD_REQUEST
    except KeyError as error: # If any required keys are missing from JSON
        return error, BAD_REQUEST

# GET - Takes JSON as input
def read(json_input=None, read_type='book-all', filter_json=None):
    try:
        if read_type == 'book-all':

            result = read_all_books()

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

            return json.dumps(json_output)

        elif read_type == 'book-genre':
            pass
        elif read_type == 'note':
            response = read_book_notes(json_input)
            return response

        elif read_type == 'filter':
            pass

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

            # Call openlibrary to pull information based on isbn
            # Will call json_cache first (will implement)
            # openlibrary_json_result = update_with_OL_data(isbn)
            # Using mock data for now
            openlibrary_json_result = {'Author_First_Name_1': 'J.R.R.', 'Author_Last_Name_1': 'Tolkien',
                                       'Author_First_Name_2': '', 'Author_Last_Name_2': '',
                                       'Author_OL_ID_1': 'OL26320A', 'Author_OL_ID_2': '',
                                       'Publisher': 'Houghton Mifflin Company', 'Publisher_OL_ID': '',
                                       'Publish_Year': '1977', 'Summary': 'A number-one New York Times bestseller when '
                                                                          'it was originally published, The Silmarillion '
                                                                          'is the core of J.R.R. Tolkien\'s imaginative '
                                                                          'writing, a work whose origins stretch back to '
                                                                          'a time long before The Hobbit. ',
                                       'Cover_Image_URL': ''}

            if json_input.get('Cover_Image_Update') is not None:
                # Download cover image fron openlibrary_json_result['Cover_Image_URL']
                # to /static/cover_image_cache and copy with cover image naming scheme
                # cover_images folder

                # Using the name from the cover_images folder, update in database
                pass

            if json_input.get('Summary_Update') is not None:
                update_book_summary(isbn, openlibrary_json_result['Summary'])

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



normal_data = {"ISBN": "0061091464",
               "Title": "The Thief of Always",
               "Publish_Year": "1993",
               "Summary": "After a mysterious stranger promises to end"
                          " his boredom with a trip to the magical Holiday"
                          " House, ten-year-old Harvey learns that his fun"
                          " has a high price.",
               "Chapters": "24",
               "Chapters_Completed": "24",
               "Cover_Image": "",
               "Author_First_Name_1": "Clive",
               "Author_Last_Name_1": "Barker",
               "Author_First_Name_2": "",
               "Author_Last_Name_2": "",
               "Publisher_Name": "HarperCollins",
               "Owned": "yes",
               "Favorite": "yes",
               "Completed": "yes",
               "Currently_Reading": "no",
               "Personal_Or_Academic": "personal",
               "Genre_1": "fiction",
               "Genre_2": "horror",
               "Genre_3": "fantasy"}



if __name__ == '__main__':
    #main()
    pass