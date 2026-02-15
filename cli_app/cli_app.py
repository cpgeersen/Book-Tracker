import create_db  # Must be first import to auto-execute database creation
from cli_app_create_book import main as cli_create_book


def main_test():
    pass

def main():


    while True:
        try:
            print('---------------------')
            print('1 - Create Book Record')
            print('2 - Read Book Record')
            print('3 - Update Book Record')
            print('4 - Delete Book Record')
            print('5 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Creating Book Record')
                cli_create_book()
            elif user_choice == 2:
                print('Reading Book Record')
                break
            elif user_choice == 3:
                print('Updating Book Record')
                #cli_read_book()
            elif user_choice == 4:
                print('Deleting Book Record')
                break
            elif user_choice == 5:
                print('Exiting')
                break
            else: # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-5: {error}')

if __name__ == '__main__':
    main()


