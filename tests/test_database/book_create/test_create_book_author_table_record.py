from app.services.Book.BookCreate import create_book_author_table_record, create_book_record
from app.services.Book.BookRead import read_author_id_from_name

book_1 = {"ISBN": "0061091464",
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

book_with_same_author = {"ISBN": "0061002828",
                         "Title": "The Hellbound Heart",
                         "Publish_Year": "1991",
                         "Summary": "",
                         "Chapters": "",
                         "Chapters_Completed": "",
                         "Cover_Image": "",
                         "Author_First_Name_1": "Clive",
                         "Author_Last_Name_1": "Barker",
                         "Author_First_Name_2": "",
                         "Author_Last_Name_2": "",
                         "Publisher_Name": "HarperTorch",
                         "Owned": "yes",
                         "Favorite": "yes",
                         "Completed": "yes",
                         "Currently_Reading": "no",
                         "Personal_Or_Academic": "personal",
                         "Genre_1": "fiction",
                         "Genre_2": "horror"}


def test_create_book_author_table_record_author_present():
    create_book_record(book_1)
    author_id = read_author_id_from_name(book_with_same_author['Author_First_Name_1'], book_with_same_author['Author_Last_Name_1'])
    response = create_book_author_table_record(book_with_same_author['ISBN'], author_id['Author_ID'])
    assert response

def test_create_book_author_table_record_author_not_present():
    create_book_record(book_1)
    author_id = read_author_id_from_name(book_1['Author_First_Name_1'], book_1['Author_Last_Name_1'])
    response = create_book_author_table_record(book_1['ISBN'], author_id['Author_ID'])
    assert response == False
















