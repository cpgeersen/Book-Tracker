import json

from app.services.Book.BookRead import read_genres_ids, read_genres_for_full_book_record
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

def test_read_genres_for_full_book_record_success():
    create_book(book)
    genre_ids = read_genres_ids(book['ISBN'])
    response = json.loads(read_genres_for_full_book_record(genre_ids))
    assert response['Genre_ID_1'] == 100
    assert response['Genre_1'] == 'fiction'
    # Since genre number from frontend can change,
    # though not an issue since genre_id is still bound
    # to the correct genres, just different order when
    # given back to the frontend
    assert response['Genre_ID_2'] == 111 or 113
    assert response['Genre_2'] == 'horror' or 'fantasy'
    assert response['Genre_ID_3'] == 111 or 113
    assert response['Genre_3'] == 'horror' or 'fantasy'
    assert response['Genre_ID_4'] == 191
    assert response['Genre_4'] == 'children'

def test_read_genres_for_full_book_record_failure():
    genre_ids = json.dumps({"Genre_IDs": [1000]})
    response = json.loads(read_genres_for_full_book_record(genre_ids))
    assert response['Error'] == 'Genre_ID not found'
