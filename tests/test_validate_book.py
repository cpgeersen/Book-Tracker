from app.services.validate_book_json import validate_book
import json

normal_data = {"ISBN": "0061091464",
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


def test_validate_book():
    result = validate_book(normal_data, 'Book')[0]
    assert result['ISBN'] == '0061091464'
    assert result['Title'] == 'The Thief of Always'
    assert result['Publish_Year'] == '1993'
    assert result['Summary'] == ("After a mysterious stranger promises to end" +
                                 " his boredom with a trip to the magical Holiday" +
                                 " House, ten-year-old Harvey learns that his fun" +
                                 " has a high price.")
    assert result['Chapters'] == '24'
    assert result['Chapters_Completed'] == '24'
    assert result['Cover_Image'] == ''
    assert result['Author_First_Name_1'] == 'Clive'
    assert result['Author_Last_Name_1'] == 'Barker'
    assert result['Author_First_Name_2'] == ''
    assert result['Author_Last_Name_2'] == ''
    assert result['Publisher_Name'] == 'HarperCollins'
    assert result['Owned'] == 'yes'
    assert result['Favorite'] == 'yes'
    assert result['Currently_Reading'] == 'no'
    assert result['Personal_Or_Academic'] == 'personal'
    assert result['Genre_1'] == 'fiction'
    assert result['Genre_2'] == 'horror'
    assert result['Genre_3'] == 'fantasy'

