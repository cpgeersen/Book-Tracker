from sample_book_entries import get_sample_books
from app.services.Book.Book import create_book, read_book


def main():
    while True:
        try:
            print('---------------------')
            print('1 - Create Example Books')
            print('2 - Create Book from User Data')
            print('3 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Creating Example Book')
                sample_books = get_sample_books()
                for book in sample_books:
                    create_book(book)
                    print(read_book(book['ISBN']))

            elif user_choice == 2:
                print('User Defined Book')
                user_book = get_user_book_input()

                create_book(user_book)
                print(read_book(user_book['ISBN']))

            elif user_choice == 3:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-3: {error}')


def get_user_book_input():
    isbn = input('Enter an ISBN: ')
    title = input('Enter a Title: ')
    publisher_year = input('Enter a Publish Year: ')
    summary = input('(Optional) Enter a Summary: ')
    chapters = input('(Optional) Enter Number of Chapters: ')
    chapters_completed = input('(Optional) Enter Number of Completed Chapters: ')
    author_first_name_1 = input('Enter Primary Author First Name: ')
    author_last_name_1 = input('Enter Primary Author Last Name: ')
    author_first_name_2 = input('(Optional) Enter Secondary Author First Name: ')
    author_last_name_2 = input('(Optional) Enter Secondary Author Last Name: ')
    publisher_name = input('Enter a Publisher Name: ')
    owned = input('Tags - Owned (yes/no): ')
    favorite = input('Tags - Favorite (yes/no): ')
    completed = input('Tags - Completed (yes/no): ')
    currently_reading = input('Tags - Currently Reading (yes/no): ')
    personal_or_academic = input('Tags - Personal or Academic (personal/academic): ')
    genre_1 = input('Genre 1 (fiction/nonfiction): ')
    genre_2 = input('(Optional) Genre 2: ')
    genre_3 = input('(Optional) Genre 3: ')
    genre_4 = input('(Optional) Genre 4: ')

    book_json = {"ISBN": isbn,
          "Title": title,
          "Publish_Year": publisher_year,
          "Summary": summary,
          "Chapters": chapters,
          "Chapters_Completed": chapters_completed,
          "Cover_Image": "",
          "Author_First_Name_1": author_first_name_1,
          "Author_Last_Name_1": author_last_name_1,
          "Author_First_Name_2": author_first_name_2,
          "Author_Last_Name_2": author_last_name_2,
          "Publisher_Name": publisher_name,
          "Owned": owned,
          "Favorite": favorite,
          "Completed": completed,
          "Currently_Reading": currently_reading,
          "Personal_Or_Academic": personal_or_academic,
          "Genre_1": genre_1,
          "Genre_2": genre_2,
          "Genre_3": genre_3,
          "Genre_4": genre_4}

    return book_json



if __name__ == '__main__':
    main()
