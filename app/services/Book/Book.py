from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record
from app.services.Book.BookDelete import delete_book_record
from app.services.Book.BookPredicate import is_isbn_in_book_table
import json


def create_book(json):
    return create_book_record(json)

def read_book(isbn):
    try:
        return read_full_book_record(isbn)
    except json.decoder.JSONDecodeError:
        return f'Error: Book with ISBN {isbn} not in database.'



def is_isbn_present(isbn):
    return is_isbn_in_book_table(isbn)

def delete_book(isbn):
    return delete_book_record(isbn)


if __name__ == '__main__':
    pass