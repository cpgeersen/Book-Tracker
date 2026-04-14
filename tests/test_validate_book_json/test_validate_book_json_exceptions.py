import pytest

from app.services.validate_json.validate_book_json import validate_book, validate_author, validate_publisher

empty_data = {}

def test_validate_book_missing_isbn():
    with pytest.raises(KeyError):
        validate_book(empty_data)

def test_validate_book_missing_title():
    empty_data.update({'ISBN': '1234567890123'})
    with pytest.raises(KeyError):
        validate_book(empty_data)

def test_validate_author_missing_author():
    empty_data.update({'Title': 'ExampleTitle'})
    with pytest.raises(KeyError):
        validate_author(empty_data)

def test_validate_publisher_missing_name():
    empty_data.update({'Author_First_Name_1': 'John'})
    empty_data.update({'Author_Last_Name_1': 'Doe'})
    with pytest.raises(KeyError):
        validate_publisher(empty_data)

def test_validate_publisher_missing_year():
    empty_data.update({'Publisher_Name': 'Example Name'})
    with pytest.raises(KeyError):
        validate_publisher(empty_data)