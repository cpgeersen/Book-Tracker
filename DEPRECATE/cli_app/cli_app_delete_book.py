from app.services.Book.Book import delete_book

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Delete a Book Using ISBN')
            print('2 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                delete_isbn = input('Enter the ISBN to delete: ')
                delete_result = delete_book(delete_isbn)
                print(delete_result)
            elif user_choice == 2:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-2: {error}')


if __name__ == '__main__':
    main()
