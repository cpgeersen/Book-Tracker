import json

from app.services.mediator import create, read

book_1 = {"ISBN": "0061091464",
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
          "Owned": "on",
          "Favorite": "on",
          "Completed": "on",
          "Currently_Reading": "off",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "horror",
          "Genre_3": "fantasy",
          "Genre_4": "children"}

book_2 = {"ISBN": "0312278497",
          "Title": "The Glass Bead Game",
          "Publish_Year": "1970",
          "Summary": "The state of Castalia is the home of an austere order of intellectuals.",
          "Chapters": "",
          "Chapters_Completed": "",
          "Cover_Image": "",
          "Author_First_Name_1": "Herman",
          "Author_Last_Name_1": "Hesse",
          "Author_First_Name_2": "",
          "Author_Last_Name_2": "",
          "Publisher_Name": "Picador",
          "Owned": "yes",
          "Favorite": "no",
          "Completed": "no",
          "Currently_Reading": "no",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "fantasy"}

def test_read_failure():
    response = read(book_1, read_type='')
    assert response == 'Error: Not a valid call'

def test_read_book_all():
    create(book_1, create_type='book-local')
    create(book_2, create_type='book-local')
    response = read(book_1, read_type='book-all')
    book_1_result = response.get('Book_Result_1')
    book_2_result = response.get('Book_Result_2')
    assert book_1_result is not None
    assert book_2_result is not None

def test_read_book_all_empty_database():
    response = read(book_1, read_type='book-all')
    assert response == {}

def test_read_book_isbn_success():
    create(book_1, create_type='book-local')
    response = json.loads(read(book_1, read_type='book-isbn'))
    assert response['Owned'] == book_1['Owned']
    assert response['Favorite'] == book_1['Favorite']
    assert response['Completed'] == book_1['Completed']
    assert response['Currently_Reading'] == book_1['Currently_Reading']

def test_read_book_isbn_failure():
    response = read(book_1, read_type='book-isbn')
    assert response is None

def test_read_book_title_success():
    create(book_1, create_type='book-local')
    response = json.loads(read(book_1, read_type='book-title'))
    assert response['Book_Result_1']['ISBN'] == book_1['ISBN']


def test_read_book_title_failure():
    response = json.loads(read(book_1, read_type='book-title'))
    assert response['Error'] == 'Title not found'

def test_read_book_author_success():
    create(book_1, create_type='book-local')
    create(book_2, create_type='book-local')
    response = json.loads(read({'Author_Last_Name': 'Barker'}, 'book-author'))
    assert response['Book_Result_1']['ISBN'] == book_1['ISBN']

def test_read_book_author_failure():
    response = json.loads(read({'Author_Last_Name': 'Barker'}, 'book-author'))
    assert response['Error'] == 'Author not found'













