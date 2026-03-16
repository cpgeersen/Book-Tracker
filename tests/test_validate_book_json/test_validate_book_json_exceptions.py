import pytest

from app.services.validate_book_json import validate_book, validate_author, validate_publisher

empty_data = {}

def test_validate_book_missing_isbn():
    with pytest.raises(KeyError):
        validate_book(empty_data)

def test_validate_book_missing_title():
    empty_data.update({'ISBN': '1'})
    with pytest.raises(KeyError):
        validate_book(empty_data)

def test_validate_author_missing_author():
    with pytest.raises(KeyError):
        validate_author(empty_data)

def test_validate_publisher_missing_name():
    with pytest.raises(KeyError):
        validate_publisher(empty_data)

def test_validate_publisher_missing_year():
    empty_data.update({'Publisher_Name': 'Example Name'})
    with pytest.raises(KeyError):
        validate_publisher(empty_data)