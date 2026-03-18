import pytest
import sqlite3
from app.services.Book.Book import create_book, delete_book
from app.services.Book.BookDelete import delete_book_record, connect_to_database

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

def test_delete_book_record_success():
    create_book(normal_data)
    response = delete_book(normal_data['ISBN'])
    assert response[1] == 200

def test_delete_book_record_failure():
    response = delete_book_record(normal_data['ISBN'])
    assert response[1] == 400
