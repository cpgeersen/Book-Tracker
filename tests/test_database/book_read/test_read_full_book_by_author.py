import json

from app.services.Book.BookRead import read_full_book_by_author
from app.services.Book.Book import create_book

book_1 = {"ISBN": "0061002828",
          "Title": "The Hellbound Heart",
          "Publish_Year": "1991",
          "Summary": "",
          "Chapters": "",
          "Chapters_Completed": "",
          "Cover_Image": "",
          "Author_First_Name_1": "Clive",
          "Author_Last_Name_1": "Barker",
          "Author_First_Name_2": "",
          "Author_Last_Name_2": "",
          "Publisher_Name": "HarperTorch",
          "Owned": "yes",
          "Favorite": "yes",
          "Completed": "yes",
          "Currently_Reading": "no",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "horror"}

book_2 = {"ISBN": "0061091464",
          "Title": "The Thief of Always",
          "Publish_Year": "1993",
          "Summary": "",
          "Chapters": "",
          "Chapters_Completed": "",
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
          "Genre_2": "horror"}

def test_read_full_book_by_author_success():
    create_book(book_1)
    create_book(book_2)
    response = json.loads(read_full_book_by_author(book_1['Author_Last_Name_1']))
    assert len(response) == 2

def test_read_full_book_by_author_failure():
    response = json.loads(read_full_book_by_author(book_1['Author_Last_Name_1']))
    assert response['Error'] == 'Author not found'












