import os
import json

from app.services.Book.BookCreate import create_book_record, create_book_genre_frontend
from app.services.Book.BookRead import (read_full_book_record, get_all_book_isbn, read_full_book_by_title,
                                        read_full_book_by_author)
from app.services.Book.BookUpdate import (update_summary, update_chapters, update_read_chapters,
                                          update_tags, update_cover_image, update_genre)
from app.services.Book.BookDelete import delete_book_record
from app.services.Book.BookNotes import create_note, read_note, update_note, delete_note, is_note_id_in_note_table
from app.services.Book.BookPredicate import is_isbn_in_book_table



def create_book(json):
    return create_book_record(json)

def create_book_genre(isbn, genre_id):
    return create_book_genre_frontend(isbn, genre_id)

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

def read_all_books_by_title(title):
    return read_full_book_by_title(title)

def read_all_books_by_author(author_last_name, author_first_name=None):
    return read_full_book_by_author(author_last_name, author_first_name)

def update_book_summary(isbn, summary):
    return update_summary(isbn, summary)

def update_book_chapters(isbn, chapters):
    return update_chapters(isbn, chapters)

def update_book_chapters_completed(isbn, chapters_completed):
    return update_read_chapters(isbn, chapters_completed)

def update_book_tags(tag_id, owned, favorite, completed, currently_reading):
    return update_tags(tag_id, owned, favorite, completed, currently_reading)

def update_book_cover_image(isbn, cover_image_path):
    return update_cover_image(isbn, cover_image_path)



def update_book_genre(isbn, old_genre_id, new_genre_id):
    return update_genre(isbn, old_genre_id, new_genre_id)

def delete_book(isbn):
    return delete_book_record(isbn)

def create_book_note(json_input):
    return create_note(json_input)

def read_book_notes(json_input):
    return read_note(json_input)

def update_book_note(json_input):
    return update_note(json_input)

def delete_book_note(json_input):
    return delete_note(json_input)

def delete_book_cover_image(isbn, cover_image_path):

    update_book_cover_image(isbn, cover_image_path='')

    try:
        os.remove(f'./app{cover_image_path}')
        return json.dumps({'Success': 'Cover image deleted'}), 200
    except OSError:
        # File does not exist
        return json.dumps({'Error': 'File does not exist'}), 200

def is_in_book_table(isbn):
    return is_isbn_in_book_table(isbn)

def is_note_id_in_database(json_input):
    return is_note_id_in_note_table(json_input)
















if __name__ == '__main__':
    pass