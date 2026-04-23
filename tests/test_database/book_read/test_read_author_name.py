import json

from app.services.Book.BookRead import read_author_name, read_author_id_from_name, read_author_id
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
          "Author_First_Name_2": "John",
          "Author_Last_Name_2": "Doe",
          "Publisher_Name": "HarperCollins",
          "Owned": "yes",
          "Favorite": "yes",
          "Completed": "yes",
          "Currently_Reading": "no",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "horror",
          "Genre_3": "fantasy"}

def test_read_author_name_success():
    create_book(book)
    author_id = read_author_id(book['ISBN'])
    response = json.loads(read_author_name(author_id))
    assert response['1'] == ['Clive', 'Barker']
    assert response['2'] == ['John', 'Doe']

def test_read_author_name_failure_author_id():
    json_dump = json.dumps({"Author_IDs": [1, 2]})
    response = json.loads(read_author_name(json_dump))
    assert response['Error'] == 'Author_ID not found'

def test_read_author_name_failure_isbn():
    author_id = read_author_id(book['ISBN'])
    response = json.loads(read_author_name(author_id))
    assert response['Error'] == 'ISBN not found'


















