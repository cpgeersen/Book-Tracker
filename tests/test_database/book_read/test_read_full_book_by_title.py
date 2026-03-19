import json

from app.services.Book.BookRead import read_full_book_by_title
from app.services.Book.Book import create_book

book_1 = {"ISBN": "9781407135397",
          "Title": "The Hunger Games",
          "Publish_Year": "2008",
          "Summary": "",
          "Chapters": "0",
          "Chapters_Completed": "24",
          "Cover_Image": "",
          "Author_First_Name_1": "Suzanne",
          "Author_Last_Name_1": "Collins",
          "Author_First_Name_2": "",
          "Author_Last_Name_2": "",
          "Publisher_Name": "Scholastic",
          "Owned": "yes",
          "Favorite": "yes",
          "Completed": "yes",
          "Currently_Reading": "no",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "science fiction",
          "Genre_3": "dystopian",
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
          "Genre_1": "fiction"}

def test_read_full_book_by_title_failure():
    create_book(book_1)
    create_book(book_2)
    response = json.loads(read_full_book_by_title('z'))
    assert response['Error'] == 'Title not found'

def test_read_full_book_by_title_failure_block():
    BLOCK_LIST = ['the', 'a', 'be', 'that', 'of', 'this', 'and', 'by']
    for value in BLOCK_LIST:
        response = json.loads(read_full_book_by_title(value))
        assert response['Error'] == 'Unable to search by that title.'

def test_read_full_book_by_title_success():
    create_book(book_1)
    create_book(book_2)
    response = json.loads(read_full_book_by_title(' game '))
    assert response[0]['ISBN'] == '9781407135397'
    assert response[1]['ISBN'] == '0312278497'


















