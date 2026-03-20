import json
from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record

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

def test_create_book_record_two_authors():
    create_book_record(book_1_with_two_authors)
    create_book_record(book_2_with_two_authors)
    book_1 = json.loads(read_full_book_record(book_1_with_two_authors['ISBN']))
    book_2 = json.loads(read_full_book_record(book_2_with_two_authors['ISBN']))
    assert book_1['Author_ID_2'] == book_2['Author_ID_2']
    assert book_1['Author_First_Name_2'] == book_2['Author_First_Name_2']
    assert book_1['Author_Last_Name_2'] == book_2['Author_Last_Name_2']