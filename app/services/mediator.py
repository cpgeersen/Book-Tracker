from app.services.validate_book_json import validate_book
from app.services.full_read_book import read_full_book_record


def main(): # Test main
    book1 = create(json1, 'book')
    print(book1)


# POST - Takes JSON as input
def create(json, create_type):
    create_type = create_type.lower()
    if create_type == 'book':
        return validate_book(json, create_type)  # the validated JSON will then be called with database INSERT here
    elif create_type == 'note':
        return 'WIP'
    else:
        return 'Error: Not a valid call'


# GET - Takes JSON as input
def read(json):
    return str(json)


# PATCH - Takes JSON as input
def update(json):
    return str(json)


# DELETE - Takes JSON as input
def delete(json):
    return str(json)

json_test = {'Author_First_Name_1': 'John',
             'Author_Last_Name_1':'Doe',
        'Chapters': 30,
        'Genre_1': 'fiction',
        'ISBN': 1234567890123,
        'Owned': 'yes',
        'Personal_Or_Academic': 'personal',
        'Publisher_Name': 'SomePublisher',
        'Title': 'BookTitle',
        'Publish_Year': '2026',}


json1 = {"ISBN": 1234567890123,
             "Title": "SomeBook",
             "Publish_Year": "2026",
             "Publisher_ID": "3",
             "Summary": "asdfdasadfsdfsafds",
             "Tag_ID": "4",
             "Chapters": "23",
             "Chapters_Completed": "3",
             "Cover_Image_Bytes": "",
             "AuthorID_1": "1",
             "Author_First_Name_1": "John",
             "Author_Last_Name_1": "Doe",
             "AuthorID_2": "4",
             "Author_First_Name_2": "Jane",
             "Author_Last_Name_2": "Doe",
             "Publisher_Name": "SomePublisher",
             "Owned": "yes",
             "Favorite": "yes",
             "Completed": "no",
             "Currently_Reading": "yes",
             "Personal_Or_Academic": "personal",
             "GenreID_1": "1",
             "Genre_1": "fiction",
             "GenreID_2": "3",
             "Genre_2": "fantasy",
             "GenreID_3": "6",
             "Genre_3": "humor",
             "GenreID_4": "4",
             "Genre_4": "drama"}

if __name__ == '__main__':
    main()