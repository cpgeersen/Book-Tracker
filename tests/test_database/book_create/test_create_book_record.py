import json
from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record


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

def test_create_book_record():
    create_book_record(book)
    book_response = json.loads(read_full_book_record(book['ISBN']))
    assert book_response['ISBN'] == book['ISBN']
    assert book_response['Title'] == book['Title']
    assert book_response['Publish_Year'] == book['Publish_Year']
    assert book_response['Summary'] == book['Summary']
    assert book_response['Chapters'] == book['Chapters']
    assert book_response['Chapters_Completed'] == book['Chapters_Completed']
    assert book_response['Cover_Image'] == book['Cover_Image']
    assert book_response['Author_First_Name_1'] == book['Author_First_Name_1']
    assert book_response['Author_Last_Name_1'] == book['Author_Last_Name_1']
    assert book_response['Publisher_Name'] == book['Publisher_Name']
    assert book_response['Owned'] == book['Owned']
    assert book_response['Favorite'] == book['Favorite']
    assert book_response['Completed'] == book['Completed']
    assert book_response['Currently_Reading'] == book['Currently_Reading']
    assert book_response['Personal_Or_Academic'] == book['Personal_Or_Academic']
    assert book_response['Genre_1'] == book['Genre_1']