import json

from app.services.mediator import create

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

def test_create_failure():
    response = create(book, create_type='')
    assert response == 'Error: Not a valid call'

def test_create_book_success():
    response = create(book, create_type='book-local')
    assert response[1] == 200


def test_create_note_success():
    create(book, create_type='book-local')
    json_input = json.dumps({'ISBN': book['ISBN'], 'Note_Content': 'note',
                             'Note_ID': ''})
    response = create(json_input, create_type='note')

    assert response == {'Note_ID': '1', 'Note_Content': 'note'}

def test_create_note_update():
    create(book, create_type='book-local')
    json_input = json.dumps({'ISBN': book['ISBN'], 'Note_Content': 'note',
                             'Note_ID': ''})
    create(json_input, create_type='note')

    json_input = json.dumps({'ISBN': book['ISBN'], 'Note_Content': 'new content',
                             'Note_ID': '1'})
    response = create(json_input, create_type='note')

    assert response == {'status': 'success'}


def test_create_note_empty():
    create(book, create_type='book-local')
    json_input = json.dumps({'ISBN': book['ISBN'], 'Note_Content': '',
                             'Note_ID': ''})
    response = json.loads(create(json_input, create_type='note'))

    assert response == {'Error': 'Empty Note'}











