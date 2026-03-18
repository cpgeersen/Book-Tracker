import json
from app.services.Book.BookRead import read_tag_table
from app.services.Book.Book import create_book

book_all_tags_no = {"ISBN": "0061091464",
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
          "Owned": "no",
          "Favorite": "no",
          "Completed": "no",
          "Currently_Reading": "no",
          "Personal_Or_Academic": "personal",
          "Genre_1": "fiction",
          "Genre_2": "horror",
          "Genre_3": "fantasy"}

book_all_tags_yes = {"ISBN": "0061091464",
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
          "Currently_Reading": "yes",
          "Personal_Or_Academic": "academic",
          "Genre_1": "fiction",
          "Genre_2": "horror",
          "Genre_3": "fantasy"}

def test_read_tag_table_all_tags_no():
    create_book(book_all_tags_no)
    response = json.loads(read_tag_table(1))
    assert  response['Owned'] == book_all_tags_no['Owned']
    assert response['Favorite'] == book_all_tags_no['Favorite']
    assert response['Completed'] == book_all_tags_no['Completed']
    assert response['Currently_Reading'] == book_all_tags_no['Currently_Reading']
    assert response['Personal_Or_Academic'] == book_all_tags_no['Personal_Or_Academic']

def test_read_tag_table_all_tags_yes():
    create_book(book_all_tags_yes)
    response = json.loads(read_tag_table(1))
    assert  response['Owned'] == book_all_tags_yes['Owned']
    assert response['Favorite'] == book_all_tags_yes['Favorite']
    assert response['Completed'] == book_all_tags_yes['Completed']
    assert response['Currently_Reading'] == book_all_tags_yes['Currently_Reading']
    assert response['Personal_Or_Academic'] == book_all_tags_yes['Personal_Or_Academic']

def test_read_tag_table_missing_tag_id():
    response = read_tag_table(1)
    assert response == 'Tag_ID not found'

















