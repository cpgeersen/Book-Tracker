from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record, get_all_book_isbn
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

def read_all_books():
    all_book_isbns = get_all_book_isbn()
    json_output = {}

    book_result_number = 1
    for book in all_book_isbns:
        result = read_book(book[0])
        json_output[f'Book_Result_{book_result_number}'] = json.loads(result)
        book_result_number += 1

    return json_output

def delete_book(isbn):
    return delete_book_record(isbn)


if __name__ == '__main__':
    read_all_books()