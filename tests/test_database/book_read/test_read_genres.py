import json

from app.services.Book.BookRead import read_genres, read_genres_ids
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

def test_read_genres_success():
    create_book(book)
    genre_ids = read_genres_ids(book['ISBN'])
    print(genre_ids)
    genres = json.loads(read_genres(genre_ids))
    assert genres == {'1': 'fiction', '111': 'fantasy', '113': 'horror', '191': 'children'}

def test_read_genres_failure():
    genre_ids = json.dumps({"Genre_IDs": [10000]})
    response = json.loads(read_genres(genre_ids))
    assert response['Error'] == 'Genre_ID not found'















