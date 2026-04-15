import json

from app.services.Book.Book import create_book, read_book
from app.services.Book.BookUpdate import update_tags

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
          "Currently_Reading": "yes",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "horror",
          "Genre_3": "fantasy",
          "Genre_4": "children"}

def test_update_tags_success():
    create_book(book)
    book_response = json.loads(read_book(book['ISBN']))
    response = update_tags(book_response['Tag_ID'], 'no', 'no', 'no',
                           'no', 'academic')
    book_response_updated = json.loads(read_book(book['ISBN']))
    assert response[1] == 200
    assert book_response_updated['Owned'] != book_response['Owned']
    assert book_response_updated['Favorite'] != book_response['Favorite']
    assert book_response_updated['Completed'] != book_response['Completed']
    assert book_response_updated['Currently_Reading'] != book_response['Currently_Reading']
    assert book_response_updated['Personal_Or_Academic'] != book_response['Personal_Or_Academic']

def test_update_tags_failure():
    response = update_tags(1, 'no', 'no', 'no', 'no',
                           'personal')
    assert response[1] == 400




























