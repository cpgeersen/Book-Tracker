from app.services.Book.BookCreate import create_book, create_tag, create_publisher
from app.services.Book.BookRead import read_publisher_id

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


def test_create_book():
    isbn = book['ISBN']
    title = book['Title']
    publisher_year = book['Publish_Year']
    publisher_name = book['Publisher_Name']
    summary = book['Summary']
    chapters = book['Chapters']
    chapters_completed = book['Chapters_Completed']
    cover_image = book['Cover_Image']
    owned = book['Owned']
    favorite = book['Favorite']
    completed = book['Completed']
    currently_reading = book['Currently_Reading']
    personal_or_academic = book['Personal_Or_Academic']

    publisher_response = read_publisher_id(publisher_name)
    if publisher_response['Publisher_ID']:
        publisher_id = publisher_response['Publisher_ID']
    else:
        publisher_id = create_publisher(publisher_name)

    tag_id = create_tag(isbn, owned, favorite, completed, currently_reading, personal_or_academic)

    book_response = create_book(isbn, title, publisher_year, publisher_id['Publisher_ID'], summary, tag_id['Tag_ID'],
                                chapters, chapters_completed, cover_image)

    assert book_response
















