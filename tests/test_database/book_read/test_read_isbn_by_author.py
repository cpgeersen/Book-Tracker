import json

from app.services.Book.BookRead import read_isbn_by_author
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

def test_read_isbn_by_author_failure():
    response = json.loads(read_isbn_by_author(book_1['Author_Last_Name_1']))
    assert response['Error'] == 'Author not found'

def test_read_isbn_by_author_success_one_author():
    create_book(book_1)
    create_book(book_2)
    response = json.loads(read_isbn_by_author(book_1['Author_Last_Name_1'], book_1['Author_First_Name_1']))
    assert response['ISBN'] == [book_1['ISBN'], book_2['ISBN']]


book_1_with_two_authors = {"ISBN": "9780671434038",
        "Title": "Mote In Gods Eye",
        "Publish_Year": "1981",
        "Summary": "",
        "Chapters": "",
        "Chapters_Completed": "",
        "Cover_Image": "",
        "Author_First_Name_1": "Larry",
        "Author_Last_Name_1": "Niven",
        "Author_First_Name_2": "Jerry",
        "Author_Last_Name_2": "Pournelle",
        "Publisher_Name": "Simon and Schuster",
        "Owned": "yes",
        "Favorite": "no",
        "Completed": "no",
        "Currently_Reading": "no",
        "Personal_Or_Academic": "personal",
        "Genre_1": "fiction",
        "Genre_2": "science fiction"}

book_2_with_two_authors = {"ISBN": "0345421396",
        "Title": "Lucifer's Hammer",
        "Publish_Year": "1998",
        "Summary": "",
        "Chapters": "",
        "Chapters_Completed": "",
        "Cover_Image": "",
        "Author_First_Name_1": "Larry",
        "Author_Last_Name_1": "Niven",
        "Author_First_Name_2": "Jerry",
        "Author_Last_Name_2": "Pournelle",
        "Publisher_Name": " Ballantine",
        "Owned": "yes",
        "Favorite": "no",
        "Completed": "no",
        "Currently_Reading": "no",
        "Personal_Or_Academic": "personal",
        "Genre_1": "fiction",
        "Genre_2": "science fiction"}

def test_read_isbn_by_author_success_two_authors():
    create_book(book_1_with_two_authors)
    create_book(book_2_with_two_authors)
    response = json.loads(read_isbn_by_author(book_1_with_two_authors['Author_Last_Name_2']))
    assert response['ISBN'] == [book_1_with_two_authors['ISBN'], book_2_with_two_authors['ISBN']]















