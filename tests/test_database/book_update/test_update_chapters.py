import json

from app.services.Book.Book import create_book, read_book
from app.services.Book.BookUpdate import update_chapters

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

def test_update_chapters_success():
    new_chapters_completed = '0'
    create_book(book)
    response = update_chapters(book['ISBN'], new_chapters_completed)
    book_chapters_updated = json.loads(read_book(book['ISBN']))
    assert response[1] == 200
    assert book_chapters_updated['Chapters'] == new_chapters_completed

def test_update_chapters_failure():
    new_chapters_completed = '0'
    response = update_chapters(book['ISBN'], new_chapters_completed)
    assert response[1] == 400



