from cli_app_create_book import main as cli_create_book
from cli_app_read_book import main as cli_read_book

def main():
    while True:
        try:
            print('---------------------')
            print('1 - Create Book Record')
            print('2 - Read Book Record')
            print('3 - Update Book Record')
            print('4 - Delete Book Record')
            print('5 - Exit')
            print('6 - Test Area')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Creating Book Record')
                cli_create_book()
            elif user_choice == 2:
                print('Reading Book Record')
                cli_read_book()
            elif user_choice == 3:
                print('Updating Book Record')
                #cli_update_book()
            elif user_choice == 4:
                print('Deleting Book Record')
                #cli_delete_book()
            elif user_choice == 5:
                print('Exiting')
                break
            elif user_choice == 6:
                print('Test Area')

            else: # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-6: {error}')

if __name__ == '__main__':
    main()


