from app.services.validate_json.validate_openlibrary_json import validate_isbn_search, validate_search_for_cache

isbn_search = {
    "ISBN": "9781594201202",
    "Title": "Against the Day",
    "Author_1": "Thomas Pynchon",
    "Author_1_OLID": "OL384171A",
    "Publisher_Name": "The Penguin Press",
    "Publisher_OLID": 'null',
    "Publish_Year": "2006",
    "Summary": "Content Text",
    "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
}

isbn_search_period_in_name = {
    "ISBN": "9781594201202",
    "Title": "Against the Day",
    "Author_1": "Thomas. Pynchon",
    "Author_1_OLID": "OL384171A",
    "Publisher_Name": "The Penguin Press",
    "Publisher_OLID": 'null',
    "Publish_Year": "2006",
    "Summary": "",
    "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
}

isbn_search_second_author = {
    "ISBN": "9781594201202",
    "Title": "Against the Day",
    "Author_1": "Thomas Pynchon",
    "Author_1_OLID": "OL384171A",
    "Author_2": "Fake Second",
    "Author_2_OLID": "OL00000A",
    "Publisher_Name": "The Penguin Press",
    "Publisher_OLID": 'null',
    "Publish_Year": "2006",
    "Summary": "",
    "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
}

isbn_search_space_in_published_year = {
    "ISBN": "9781594201202",
    "Title": "Against the Day",
    "Author_1": "Thomas Pynchon",
    "Author_1_OLID": "OL384171A",
    "Publisher_Name": "The Penguin Press",
    "Publisher_OLID": 'null',
    "Publish_Year": "September, 2006",
    "Summary": "",
    "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
}

multiple_result = {
    "Book_Result_1": {
        "ISBN": "9781594201202",
        "Title": "Against the Day",
        "Author_1": "Thomas Pynchon",
        "Author_1_OLID": "OL384171A",
        "Publisher_Name": "The Penguin Press",
        "Publisher_OLID": "null",
        "Publish_Year": "2006",
        "Summary": "",
        "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
    },
    "Book_Result_2": {
        "ISBN": "9781594201202",
        "Title": "Against the Day",
        "Author_1": "Thomas Pynchon",
        "Author_1_OLID": "OL384171A",
        "Publisher_Name": "The Penguin Press",
        "Publisher_OLID": "null",
        "Publish_Year": "2006",
        "Summary": "",
        "Cover_Image_URL": "https://covers.openlibrary.org/b/id/872335-L.jpg"
    }
}


def test_validate_isbn_search_success():
    response = validate_isbn_search(isbn_search, isbn=None)
    assert response.get('Author_First_Name_1') is not None


def test_validate_isbn_search_title_failure():
    response = validate_isbn_search({}, isbn=None)
    assert response == {}


def test_validate_isbn_search_author_failure():
    response = validate_isbn_search({"Title": "Against the Day"}, isbn=None)
    assert response == {}


def test_validate_isbn_search_author_period_case():
    response = validate_isbn_search(isbn_search_period_in_name, isbn=None)
    assert response.get('Author_First_Name_1') == 'Thomas'


def test_validate_isbn_search_second_author():
    response = validate_isbn_search(isbn_search_second_author, isbn=None)
    assert response.get('Author_First_Name_2') is not None


def test_validate_isbn_search_space_in_publisher_year():
    response = validate_isbn_search(isbn_search_space_in_published_year, isbn=None)
    assert response.get('Publish_Year') == '2006'


def test_validate_multiple_result():
    response = validate_search_for_cache(multiple_result)
    assert response.get('Book_Result_1') is not None
    assert response.get('Book_Result_2') is not None
