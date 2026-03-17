from app.services.Book.BookCreate import create_book_record

book_missing_tags_and_genres = {"ISBN": "0312278497",
          "Title": "The Glass Bead Game",
          "Publish_Year": "1970",
          "Summary": "The state of Castalia is the home of an austere order of intellectuals.",
          "Chapters": "",
          "Chapters_Completed": "",
          "Cover_Image": "",
          "Author_First_Name_1": "Herman",
          "Author_Last_Name_1": "Hesse",
          "Author_First_Name_2": "",
          "Author_Last_Name_2": "",
          "Publisher_Name": "Picador"}

def test_create_book_record_missing_tags():
    response = create_book_record(book_missing_tags_and_genres)
    assert response[1] == 200