from app.services.Book.BookCreate import create_book_genre_table_record
from app.services.Book.BookRead import read_genre_id_from_genre_table

book_with_repeated_genres = {"ISBN": "0061091464",
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
          "Genre_3": "horror"}

def test_create_book_genre_table_record():
    isbn = book_with_repeated_genres['ISBN']
    genre_2 = book_with_repeated_genres['Genre_2']
    genre_3 = book_with_repeated_genres['Genre_3']
    genre_2_id = read_genre_id_from_genre_table(genre_2)
    genre_3_id = read_genre_id_from_genre_table(genre_3)

    genre_2_response = create_book_genre_table_record(isbn, genre_2_id)
    genre_3_response = create_book_genre_table_record(isbn, genre_3_id)
    assert genre_2_response
    assert genre_3_response == False


