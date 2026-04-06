import json
from app.services.validate_book_json import validate_book_from_local, validate_book_for_frontend, validate_tags
from app.services.Book.Book import (create_book, read_book, read_all_books, read_all_books_by_title,
                                    read_all_books_by_author, update_book_summary, update_book_chapters,
                                    update_book_chapters_completed, update_book_tags, delete_book)
from app.services.openlibrary_api import search_books_by_title, get_work_data

SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

#def main(): # Test main
    #result = create(normal_data, 'book-local')
    #print(result)
    #print(read_book('0061091464'))
    #print(read())
    #pass


def complete_book_from_ol(query,):
    #searh by title
    search_results = search_books_by_title(query=query)
    #search fails
    if "error" in search_results:
        return search_results
    #search succeeds, return search results for user to select from
    docs = search_results['docs']
    if 'docs' not in search_results:
        return {"error": "No search results found for the given title."}
        #create_book(json) #should we handle 3.2.2 like this ?
    
    if len(docs) == 0:
        return {"error": "No search results found for the given title."}
    #testing first result
    first_result = docs[0]
    book_title = first_result.get('title')
    first_publish_year = first_result.get('first_publish_year')    
    isbn_list = first_result.get('isbn', [])

    # now works api 
    work_key = first_result.get('key')
    author_olids = []
    if work_key:
        # Get work data from imported function, which will include author OLIDs
        work_data = get_work_data(work_key)
        #check if work_data is a dict and contains "authors" key before trying to access it PS. ALL API CALLS IN OL ARE Dictionaries
        if isinstance(work_data, dict) and "authors" in work_data:
            # Loop through authors in work data and extract OLIDs
            for author in work_data["authors"]:
                #check if "author" key exists and is a dict, and if it contains "key" before trying to access it
                if "author" in author and "key" in author["author"]:
                    # If all checks pass, append the author OLID to the list
                    author_olids.append(author["author"]["key"])

    complete_book_json = {
            "title": book_title,
            "publish_year": first_publish_year,
            "isbn_list": isbn_list,
            "work_key": work_key,
            "author_olids": author_olids,
            "first_publish_year": first_publish_year
        }
    return complete_book_json

# POST - Takes JSON as input
def create(json_input, create_type):
    try:
        if create_type == 'book-local':
            json_input = validate_book_from_local(json_input)
            result = create_book(json_input)
            return result

        elif create_type == 'book-ol':
            return 'WIP'
        elif create_type == 'note':
            return 'WIP'
        elif create_type == 'cover-image':
            return 'WIP'
        else:
            return 'Error: Not a valid call'
    except (TypeError, ValueError, AttributeError):
        return f'Error: Invalid Entry, could not parse. Try again.', BAD_REQUEST
    except KeyError as error: # If any required keys are missing from JSON
        return error, BAD_REQUEST

# GET - Takes JSON as input
def read(json_input=None, read_type='book-all'):
    try:
        if read_type == 'book-all':
            result = read_all_books()
            return result

        elif read_type == 'book-isbn':
            # First get the book record via ISBN
            result = read_book(json_input['ISBN'])
            # Then convert to frontend syntax for tags
            converted_result = validate_book_for_frontend(result)
            return converted_result

        elif read_type == 'book-title':
            all_books_by_title = json.loads(read_all_books_by_title(json_input['Title']))

            if not isinstance(all_books_by_title, list):
                return json.dumps({"Error": "Title not found", "Status_Code": "404"})

            json_output = {}
            book_result_number = 1
            for book in all_books_by_title:
                json_output[f'Book_Result_{book_result_number}'] = book
                book_result_number += 1

            return json.dumps(json_output)

        elif read_type == 'book-author':
            all_books_by_author = json.loads(read_all_books_by_author(json_input['Author_Last_Name'],
                                                           json_input.get('Author_First_Name')))

            if not isinstance(all_books_by_author, list):
                return json.dumps({"Error": "Author not found", "Status_Code": "404"})

            json_output = {}
            book_result_number = 1
            for book in all_books_by_author:
                json_output[f'Book_Result_{book_result_number}'] = book
                book_result_number += 1

            return json.dumps(json_output)

        elif read_type == 'book-genre':
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


    except TypeError:
        pass


# DELETE - Takes JSON as input
def delete(json_input):
    json_input = json.loads(json_input)
    response = delete_book(json_input['ISBN'])
    return response





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