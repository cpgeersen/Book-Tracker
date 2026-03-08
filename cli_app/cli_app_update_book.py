from app.services.Book.BookUpdate import update_tags, update_summary, update_chapters, update_read_chapters
from app.services.Book.Book import read_book
import json

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Update Book Tags')
            print('2 - Update Book Summary')
            print('3 - Update Book Chapters')
            print('4 - Update Book Chapters Completed')
            print('5 - Update Book Genre')
            print('6 - Update Book Cover Image')
            print('7 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Update Book Tags')
                book_isbn = input('Enter a Book ISBN to Update Tags: ')
                tag_update = get_tag_input(book_isbn)
                update_tag_response = update_tags(*tag_update)
                print(update_tag_response)

            elif user_choice == 2:
                print('Update Book Summary')
                book_isbn = input('Enter a Book ISBN to Update Summary: ')
                book_summary = input('Enter a Summary: ')
                update_summary_response = update_summary(book_isbn, book_summary)
                print(update_summary_response)

            elif user_choice == 3:
                print('Update Book Chapters')
                book_isbn = input('Enter a Book ISBN to Update the Number of Chapters: ')
                book_chapters = input('Enter the Number of Chapters: ')
                update_chapters_response = update_chapters(book_isbn, book_chapters)
                print(update_chapters_response)

            elif user_choice == 4:
                print('Update Book Chapters Completed')
                book_isbn = input('Enter a Book ISBN to Update Number of Completed Chapters: ')
                book_chapters_completed = input('Enter the Number of Completed Chapters: ')
                update_chapters_completed_response = update_read_chapters(book_isbn, book_chapters_completed)
                print(update_chapters_completed_response)

            elif user_choice == 5:
                print('Update Book Genre')
                print('WIP')
                continue

            elif user_choice == 6:
                print('Update Book Cover Image')
                print('WIP')
                continue

            elif user_choice == 7:
                print('Exiting')
                break

            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-6: {error}')

def get_tag_input(isbn):
    tag_id = json.loads(read_book(isbn))['Tag_ID']
    print(tag_id)

    owned = input('Tags - Owned (yes/no): ')
    favorite = input('Tags - Favorite (yes/no): ')
    completed = input('Tags - Completed (yes/no): ')
    currently_reading = input('Tags - Currently Reading (yes/no): ')
    personal_or_academic = input('Tags - Personal or Academic (personal/academic): ')

    return tag_id, owned, favorite, completed, currently_reading, personal_or_academic


if __name__ == 'main':
    main()