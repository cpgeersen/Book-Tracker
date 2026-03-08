from app.services.Book.BookUpdate import update_tags
from app.services.Book.Book import read_book
import json

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Update Book Tags')
            print('2 - Create Book from User Data')
            print('3 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Update Book Tags')
                book_isbn = input('Enter a Book ISBN to Update Tags: ')
                tag_update = get_tag_input(book_isbn)
                update_tag_response = update_tags(*tag_update)
                print(update_tag_response)

            elif user_choice == 2:
                print('User Defined Book')


            elif user_choice == 3:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-3: {error}')

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