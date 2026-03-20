import json

from app.services.Book.BookRead import read_publisher_name_for_full_book_record
from app.services.Book.Book import create_book

book = {"ISBN": "0061091464",
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
          "Genre_3": "fantasy",
          "Genre_4": "children"}


def test_read_publisher_name_for_full_book_record_success():
    create_book(book)
    response = json.loads(read_publisher_name_for_full_book_record(1))
    assert response['Publisher_Name'] == 'HarperCollins'


def test_read_publisher_name_for_full_book_record_failure():
    response = json.loads(read_publisher_name_for_full_book_record(1))
    assert response['Error'] == 'Publisher_ID not found'



















