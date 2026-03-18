import json

from app.services.Book.BookRead import read_publisher_name, read_publisher_id
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
          "Genre_3": "fantasy"}

def test_read_publisher_name():
    create_book(book)
    pub_id = read_publisher_id(book['Publisher_Name'])
    pub_name = json.loads(read_publisher_name(pub_id['Publisher_ID'][0]))
    assert pub_name[str(pub_id['Publisher_ID'][0])] == book['Publisher_Name']

def test_read_publisher_name_missing():
    pub_id = read_publisher_id(book['Publisher_Name'])
    response = read_publisher_name(pub_id['Publisher_ID'])
    assert response == 'Publisher_ID not found'













