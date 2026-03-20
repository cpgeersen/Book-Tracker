from app.services.Book.Book import create_book
from app.services.Book.BookPredicate import is_tag_id_in_tag_table

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
        "Genre_4": "child"}


def test_is_isbn_in_book_table_true():
    create_book(book)
    response = is_tag_id_in_tag_table(1)
    assert response

def test_is_isbn_in_book_table_false():
    response = is_tag_id_in_tag_table(1)
    assert not response