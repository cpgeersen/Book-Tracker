import json
from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record


book_1_with_same_publisher = {"ISBN": "1234567890123",
        "Title": "Best Book",
        "Publish_Year": "1997",
        "Publisher_Name": "House",
        "Author_First_Name_1": "John",
        "Author_Last_Name_1": "Doe",
        "Personal_Or_Academic": "personal",
        "Genre_1": "fiction"}
book_2_with_same_publisher = {"ISBN": "0987654321098",
        "Title": "Better Book",
        "Publish_Year": "1999",
        "Publisher_Name": "House",
        "Author_First_Name_1": "John",
        "Author_Last_Name_1": "Doe",
        "Personal_Or_Academic": "personal",
        "Genre_1": "fiction"}

def test_create_book_record_same_publisher():
    create_book_record(book_1_with_same_publisher)
    create_book_record(book_2_with_same_publisher)
    book_1 = json.loads(read_full_book_record(book_1_with_same_publisher['ISBN']))
    book_2 = json.loads(read_full_book_record(book_2_with_same_publisher['ISBN']))
    assert book_1['Publisher_Name'] == book_2['Publisher_Name']
    assert book_1['Publisher_ID'] == book_2['Publisher_ID']