from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record
from app.services.Book.BookDelete import delete_book_record
from app.services.Book.BookPredicate import is_isbn_in_book_table
import json


def create_book(json):
    print('create')
    return create_book_record(json)

def read_book(isbn):
    try:
        result = read_full_book_record(isbn)
        print('read')
        return result
    except json.decoder.JSONDecodeError:
        return f'Error: Book with ISBN {isbn} not in database.'



def is_isbn_present(isbn):
    return is_isbn_in_book_table(isbn)

def delete_book(isbn):
    return delete_book_record(isbn)

