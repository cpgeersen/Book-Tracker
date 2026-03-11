from app.services.validate_book_json import validate_book_from_local, validate_book_for_frontend
from app.services.Book.Book import create_book, read_book
import json


SUCCESS = 200
BAD_REQUEST = 400
INTERNAL_SERVER_ERROR = 500

def main(): # Test main
    result = create(normal_data, 'book-local')
    #print(result)
    #print(read_book('0061091464'))
    print(read(normal_data, 'book-isbn'))


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
    except TypeError and ValueError:
        return f'Error: Invalid Entry, could not parse. Try again.', BAD_REQUEST
    except KeyError as error: # If any required keys are missing from JSON
        return error, BAD_REQUEST

# GET - Takes JSON as input
def read(json_input, read_type):
    try:
        if read_type == 'book-all':
            pass
        elif read_type == 'book-isbn':
            # First get the book record via ISBN
            result = read_book(json_input['ISBN'])
            # Then convert to frontend syntax for tags
            converted_result = validate_book_for_frontend(result)
            return converted_result
        elif read_type == 'book-title':
            pass
        elif read_type == 'book-author':
            pass
        elif read_type == 'book-genre':
            pass
        else:
            return 'Error: Not a valid call'
    except:
        'TEMP EXCEPT'




# PATCH - Takes JSON as input
def update(json):
    return str(json)


# DELETE - Takes JSON as input
def delete(json):
    return str(json)

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
    main()