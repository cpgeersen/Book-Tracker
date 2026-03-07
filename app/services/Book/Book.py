from app.services.Book.BookCreate import create_book_record
from app.services.Book.BookRead import read_full_book_record
from app.services.Book.BookPredicate import is_isbn_in_book_table


def create_book(json):
    return create_book_record(json)

def read_book(isbn):
    return read_full_book_record(isbn)

def is_isbn_present(isbn):
    return is_isbn_in_book_table(isbn)


if __name__ == '__main__':
    pass
