from app.services.validate_book_json import validate_tags, validate_book_for_frontend
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

backend_tags = {"Owned": "yes",
                "Favorite": "yes",
                "Completed": "yes",
                "Currently_Reading": "no"}

frontend_tags = {"Owned": "on",
                "Favorite": "on",
                "Completed": "on",
                "Currently_Reading": "off"}

def test_validate_tags():
    result = validate_tags(frontend_tags)
    assert result['Owned'] == 'yes'
    assert result['Favorite'] == 'yes'
    assert result['Completed'] == 'yes'
    assert result['Currently_Reading'] == 'no'

def test_validate_book_for_frontend_str():
    backend_tags_str = json.dumps(backend_tags)
    result = json.loads(validate_book_for_frontend(backend_tags_str))
    assert result['Owned'] == 'on'
    assert result['Favorite'] == 'on'
    assert result['Completed'] == 'on'
    assert result['Currently_Reading'] == 'off'

def test_validate_book_for_frontend():
    result = json.loads(validate_book_for_frontend(backend_tags))
    assert result['Owned'] == 'on'
    assert result['Favorite'] == 'on'
    assert result['Completed'] == 'on'
    assert result['Currently_Reading'] == 'off'

